# -*- coding: utf-8 -*-
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

# Try to import Vibrator
try:
    from plyer import vibrator
except Exception:
    vibrator = None

# Cheer sound duration
CHEER_DURATION = 2.0

# App colors
BG_COLOR = (0.96, 0.96, 0.98, 1)
TITLE_COLOR = (0.15, 0.15, 0.25, 1)
BUTTON_H = 0.13


# ═══════════════════════════════════════════════
# SPLASH SCREEN
# ═══════════════════════════════════════════════
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(size_hint=(1, 0.1), text=''))

        self.photo = Image(
            source='images/app_icon.png',
            size_hint=(1, 0.55),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.photo)

        welcome = Label(
            text="Welcome to Ahmed's World!",
            font_size='26sp',
            bold=True,
            color=TITLE_COLOR,
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        welcome.bind(size=welcome.setter('text_size'))
        layout.add_widget(welcome)

        loading = Label(
            text="Loading...",
            font_size='18sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.1),
            halign='center'
        )
        layout.add_widget(loading)

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.go_to_menu, 2.5)

    def go_to_menu(self, dt):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main_menu'


# ═══════════════════════════════════════════════
# MAIN MENU SCREEN
# ═══════════════════════════════════════════════
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_box = BoxLayout(orientation='vertical', padding=20, spacing=12)

        title_box = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        title = Label(
            text="Ahmed's World",
            font_size='34sp',
            bold=True,
            color=(0.2, 0.4, 0.7, 1),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        title_box.add_widget(title)
        main_box.add_widget(title_box)

        buttons_box = BoxLayout(orientation='vertical', spacing=12, size_hint=(1, 0.85))

        btn_routine = Button(
            text="Bathroom Routine",
            font_size='22sp', bold=True,
            background_color=(0.2, 0.7, 0.9, 1),
            background_normal='',
            size_hint=(1, BUTTON_H),
            color=(1, 1, 1, 1)
        )
        btn_routine.bind(on_press=lambda x: self.goto('toilet_routine'))
        buttons_box.add_widget(btn_routine)

        btn_aac = Button(
            text="I Want",
            font_size='22sp', bold=True,
            background_color=(0.3, 0.8, 0.4, 1),
            background_normal='',
            size_hint=(1, BUTTON_H),
            color=(1, 1, 1, 1)
        )
        btn_aac.bind(on_press=lambda x: self.goto('aac_board'))
        buttons_box.add_widget(btn_aac)

        btn_quiz = Button(
            text="Quiz Game",
            font_size='22sp', bold=True,
            background_color=(0.9, 0.6, 0.2, 1),
            background_normal='',
            size_hint=(1, BUTTON_H),
            color=(1, 1, 1, 1)
        )
        btn_quiz.bind(on_press=lambda x: self.goto('quiz_game'))
        buttons_box.add_widget(btn_quiz)

        btn_memory = Button(
            text="Memory Game",
            font_size='22sp', bold=True,
            background_color=(0.7, 0.3, 0.8, 1),
            background_normal='',
            size_hint=(1, BUTTON_H),
            color=(1, 1, 1, 1)
        )
        btn_memory.bind(on_press=lambda x: self.goto('memory_game'))
        buttons_box.add_widget(btn_memory)

        btn_exit = Button(
            text="Exit",
            font_size='20sp', bold=True,
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            size_hint=(1, BUTTON_H),
            color=(1, 1, 1, 1)
        )
        btn_exit.bind(on_press=self.exit_app)
        buttons_box.add_widget(btn_exit)

        main_box.add_widget(buttons_box)
        self.add_widget(main_box)

    def goto(self, screen_name):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = screen_name

    def exit_app(self, instance):
        if platform == 'android':
            from android import mActivity
            mActivity.finish()
        else:
            App.get_running_app().stop()


# ═══════════════════════════════════════════════
# BATHROOM ROUTINE SCREEN
# ═══════════════════════════════════════════════
class ToiletRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = [
            {"text": "1. I feel the need", "image": "images/step1_feel.png", "audio": "audio/audio1.wav"},
            {"text": "2. I walk to the bathroom", "image": "images/step2_walk.png", "audio": "audio/audio2.wav"},
            {"text": "3. I pull down my pants", "image": "images/step3_pants_down.png", "audio": "audio/audio3.wav"},
            {"text": "4. I sit and wait", "image": "images/step4_sit.png", "audio": "audio/audio4.wav"},
            {"text": "5. I clean myself", "image": "images/step5_clean.png", "audio": "audio/audio5.wav"},
            {"text": "6. I pull up my pants", "image": "images/step6_pants_up.png", "audio": "audio/audio6.wav"},
            {"text": "7. I wash my hands", "image": "images/step7_wash_hands.png", "audio": "audio/audio7.wav"}
        ]
        self.current_step = 0
        self.current_sound = None
        self.layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp', bold=True,
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=self.steps[0]["text"],
            font_size='24sp', bold=True,
            color=(0.15, 0.15, 0.25, 1),
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.img = Image(
            source=self.steps[0]["image"],
            size_hint=(1, 0.62),
            allow_stretch=True,
            keep_ratio=True,
            nocache=True
        )
        self.layout.add_widget(self.img)

        self.btn_next = Button(
            text="Done!",
            font_size='26sp', bold=True,
            background_color=(0.2, 0.8, 0.2, 1),
            background_normal='',
            size_hint=(1, 0.15),
            color=(1, 1, 1, 1)
        )
        self.btn_next.bind(on_press=self.next_step)
        self.layout.add_widget(self.btn_next)

        self.add_widget(self.layout)

    def on_enter(self):
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = self.steps[0]["text"]
            self.img.source = self.steps[0]["image"]
            self.btn_next.text = "Done!"
        Clock.schedule_once(lambda dt: self.play_step_audio(), 0.5)

    def play_step_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        if 0 <= self.current_step < len(self.steps):
            sound = SoundLoader.load(self.steps[self.current_step]["audio"])
            if sound:
                self.current_sound = sound
                sound.play()

    def next_step(self, instance):
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = self.steps[0]["text"]
            self.img.source = self.steps[0]["image"]
            self.btn_next.text = "Done!"
            self.play_step_audio()
            return

        cheer = SoundLoader.load('audio/cheer.wav')
        if cheer:
            cheer.play()

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.label.text = self.steps[self.current_step]["text"]
            self.img.source = self.steps[self.current_step]["image"]
            Clock.schedule_once(lambda dt: self.play_step_audio(), CHEER_DURATION)
        else:
            Clock.schedule_once(lambda dt: self.show_final_message(), CHEER_DURATION)

    def show_final_message(self):
        self.label.text = "Amazing! You're a champion!"
        self.btn_next.text = "Restart"
        self.current_step = -1

    def go_home(self, instance):
        self.current_step = 0
        self.label.text = self.steps[0]["text"]
        self.img.source = self.steps[0]["image"]
        self.btn_next.text = "Done!"
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_menu'


# ═══════════════════════════════════════════════
# AAC BOARD SCREEN (I Want)
# ═══════════════════════════════════════════════
class AACBoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None

        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp', bold=True,
            size_hint=(1, 0.07),
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=lambda x: self.go_home())
        main_layout.add_widget(btn_back)

        self.preview = Image(
            source='images/app_icon.png',
            size_hint=(1, 0.35),
            allow_stretch=True,
            keep_ratio=True
        )
        main_layout.add_widget(self.preview)

        grid = GridLayout(cols=3, spacing=8, size_hint=(1, 0.58))

        self.cards = [
            {"title": "Ahmed", "audio": "audio/say_ahmed.wav", "image": "images/aac_ahmed.png", "color": (0.2, 0.7, 0.9, 1)},
            {"title": "Dad Emad", "audio": "audio/say_dad.wav", "image": "images/aac_dad.png", "color": (0.3, 0.8, 0.4, 1)},
            {"title": "Mohamed", "audio": "audio/say_mohamed.wav", "image": "images/aac_mohamed.png", "color": (0.2, 0.8, 0.7, 1)},
            {"title": "Milad", "audio": "audio/say_milad.wav", "image": "images/aac_milad.png", "color": (0.9, 0.5, 0.7, 1)},
            {"title": "Water", "audio": "audio/say_water.wav", "image": "images/aac_water.png", "color": (0.2, 0.6, 0.9, 1)},
            {"title": "Food", "audio": "audio/say_food.wav", "image": "images/aac_food.png", "color": (1, 0.6, 0.2, 1)},
            {"title": "Toilet", "audio": "audio/say_toilet.wav", "image": "images/aac_toilet.png", "color": (0.4, 0.6, 0.8, 1)},
            {"title": "Sleep", "audio": "audio/say_sleep.wav", "image": "images/aac_sleep.png", "color": (0.6, 0.4, 0.8, 1)},
            {"title": "Help", "audio": "audio/say_help.wav", "image": "images/aac_help.png", "color": (0.9, 0.3, 0.3, 1)},
            {"title": "Play", "audio": "audio/say_play.wav", "image": "images/aac_play.png", "color": (0.3, 0.8, 0.3, 1)},
            {"title": "Stop", "audio": "audio/say_stop.wav", "image": "images/aac_stop.png", "color": (0.8, 0.2, 0.2, 1)},
            {"title": "Happy", "audio": "audio/say_happy.wav", "image": "images/aac_happy.png", "color": (1, 0.4, 0.6, 1)},
        ]

        for card in self.cards:
            btn = Button(
                text=card["title"],
                font_size='14sp', bold=True,
                background_color=card["color"],
                background_normal='',
                size_hint=(1, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda instance, c=card: self.play_phrase(c))
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def play_phrase(self, card):
        try:
            self.preview.source = card["image"]
        except Exception:
            pass
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        sound = SoundLoader.load(card["audio"])
        if sound:
            self.current_sound = sound
            sound.play()

    def go_home(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_menu'


# ═══════════════════════════════════════════════
# QUIZ GAME SCREEN
# ═══════════════════════════════════════════════
class QuizGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None
        # ⚠️ كل الخيارات هي صور أشخاص (وليس ماء/طعام)
        self.questions = [
            {
                "question": "Where is Ahmed?",
                "audio": "audio/q_ahmed.wav",
                "correct": "images/aac_ahmed.png",
                "options": ["images/aac_milad.png", "images/aac_ahmed.png", "images/aac_mohamed.png"]
            },
            {
                "question": "Where is Mohamed?",
                "audio": "audio/q_mohamed.wav",
                "correct": "images/aac_mohamed.png",
                "options": ["images/aac_ahmed.png", "images/aac_mohamed.png", "images/aac_milad.png"]
            },
            {
                "question": "Where is Milad?",
                "audio": "audio/q_milad.wav",
                "correct": "images/aac_milad.png",
                "options": ["images/aac_mohamed.png", "images/aac_milad.png", "images/aac_ahmed.png"]
            },
            {
                "question": "Where is Dad Emad?",
                "audio": "audio/q_dad.wav",
                "correct": "images/aac_dad.png",
                "options": ["images/aac_dad.png", "images/aac_ahmed.png", "images/aac_mohamed.png"]
            }
        ]
        self.current_q = 0

        self.layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp', bold=True,
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=self.questions[0]["question"],
            font_size='26sp', bold=True,
            color=(0.15, 0.15, 0.25, 1),
            size_hint=(1, 0.12),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.8))
        self.update_options()
        self.layout.add_widget(self.grid)

        self.add_widget(self.layout)

    def on_enter(self):
        self.current_q = 0
        self.label.text = self.questions[0]["question"]
        self.update_options()
        Clock.schedule_once(lambda dt: self.play_q_audio(), 0.5)

    def play_q_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        sound = SoundLoader.load(self.questions[self.current_q]["audio"])
        if sound:
            self.current_sound = sound
            sound.play()

    def update_options(self):
        """إصلاح: صور بدل أزرار - تظهر بحجم كامل"""
        self.grid.clear_widgets()
        q_data = self.questions[self.current_q]
        for opt in q_data["options"]:
            img = Image(
                source=opt,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
                nocache=True
            )
            img.bind(on_touch_down=lambda inst, touch, i=opt: self.on_image_click(inst, touch, i))
            self.grid.add_widget(img)

    def on_image_click(self, instance, touch, img_path):
        if instance.collide_point(*touch.pos):
            self.check_answer(img_path)
            return True
        return False

    def check_answer(self, selected_img):
        correct_img = self.questions[self.current_q]["correct"]
        if selected_img == correct_img:
            cheer = SoundLoader.load('audio/cheer.wav')
            if cheer:
                cheer.play()
            if self.current_q < len(self.questions) - 1:
                self.current_q += 1
                self.label.text = self.questions[self.current_q]["question"]
                self.update_options()
                Clock.schedule_once(lambda dt: self.play_q_audio(), CHEER_DURATION)
            else:
                self.label.text = "Excellent! All questions done!"
                self.grid.clear_widgets()
        else:
            self.play_q_audio()

    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_menu'


# ═══════════════════════════════════════════════
# MEMORY GAME SCREEN
# ═══════════════════════════════════════════════
class MemoryGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.score = 0
        self.sound_enabled = True
        self.current_sound = None

        main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)

        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.09), spacing=8)

        btn_back = Button(
            text="Back",
            font_size='16sp', bold=True,
            size_hint_x=0.28,
            background_color=(0.8, 0.3, 0.3, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        btn_back.bind(on_press=lambda x: self.go_home())
        header.add_widget(btn_back)

        self.score_label = Label(
            text="Score: 0",
            font_size='18sp', bold=True,
            color=(0.15, 0.15, 0.25, 1),
            size_hint_x=0.44
        )
        header.add_widget(self.score_label)

        self.sound_btn = Button(
            text="Sound: ON",
            font_size='13sp', bold=True,
            size_hint_x=0.28,
            background_color=(0.2, 0.6, 0.9, 1),
            background_normal='',
            color=(1, 1, 1, 1)
        )
        self.sound_btn.bind(on_press=self.toggle_sound)
        header.add_widget(self.sound_btn)

        main_layout.add_widget(header)

        self.grid = GridLayout(cols=4, spacing=6, size_hint=(1, 0.83))
        main_layout.add_widget(self.grid)

        self.add_widget(main_layout)

    def on_enter(self):
        if not self.cards:
            self.start_new_game()

    def go_home(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_menu'

    def toggle_sound(self, instance):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.text = "Sound: ON" if self.sound_enabled else "Sound: OFF"

    def play_sound(self, sound_file):
        if self.sound_enabled:
            if os.path.exists(sound_file):
                if self.current_sound:
                    try:
                        self.current_sound.stop()
                    except Exception:
                        pass
                sound = SoundLoader.load(sound_file)
                if sound:
                    self.current_sound = sound
                    sound.play()

    def trigger_vibration(self, time_sec=0.05):
        if platform == 'android' and vibrator:
            try:
                vibrator.vibrate(time_sec)
            except Exception:
                pass

    def start_new_game(self):
        self.grid.clear_widgets()
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.score = 0
        self.score_label.text = "Score: 0"

        card_values = list(range(1, 7)) * 2
        random.shuffle(card_values)

        for val in card_values:
            btn = Button(
                text="?",
                font_size='28sp', bold=True,
                background_color=(0.3, 0.3, 0.5, 1),
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.val = val
            btn.is_matched = False
            btn.bind(on_press=self.on_card_click)
            self.cards.append(btn)
            self.grid.add_widget(btn)

    def on_card_click(self, btn):
        if btn in self.selected_cards or btn.is_matched or len(self.selected_cards) >= 2:
            return
        self.trigger_vibration(0.03)
        btn.text = str(btn.val)
        btn.background_color = (0.9, 0.9, 0.9, 1)
        btn.color = (0.15, 0.15, 0.25, 1)
        self.selected_cards.append(btn)
        if len(self.selected_cards) == 2:
            self.check_match()

    def check_match(self):
        c1, c2 = self.selected_cards
        if c1.val == c2.val:
            c1.is_matched = True
            c2.is_matched = True
            c1.background_color = (0.2, 0.8, 0.2, 1)
            c2.background_color = (0.2, 0.8, 0.2, 1)
            c1.color = (1, 1, 1, 1)
            c2.color = (1, 1, 1, 1)
            self.score += 10
            self.matched_pairs += 1
            self.score_label.text = f"Score: {self.score}"
            self.play_sound("audio/audio1.wav")
            self.trigger_vibration(0.1)
            self.selected_cards = []
            if self.matched_pairs == 6:
                self.score_label.text = f"Victory! Score: {self.score}"
                self.play_sound("audio/cheer.wav")
        else:
            self.score = max(0, self.score - 2)
            self.score_label.text = f"Score: {self.score}"
            Clock.schedule_once(self.reset_selected, 0.8)

    def reset_selected(self, dt):
        for btn in self.selected_cards:
            if not btn.is_matched:
                btn.text = "?"
                btn.background_color = (0.3, 0.3, 0.5, 1)
                btn.color = (1, 1, 1, 1)
        self.selected_cards = []


# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
class AhmedWorldApp(App):
    def build(self):
        self.title = "Ahmed's World"
        Window.clearcolor = (0.96, 0.96, 0.98, 1)

        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(ToiletRoutineScreen(name='toilet_routine'))
        sm.add_widget(AACBoardScreen(name='aac_board'))
        sm.add_widget(QuizGameScreen(name='quiz_game'))
        sm.add_widget(MemoryGameScreen(name='memory_game'))
        sm.current = 'splash'
        return sm

    def on_start(self):
        Window.clearcolor = (0.96, 0.96, 0.98, 1)


if __name__ == '__main__':
    AhmedWorldApp().run()
