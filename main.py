# -*- coding: utf-8 -*-
import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

# Try to import Vibrator for Memory Game
try:
    from plyer import vibrator
except Exception:
    vibrator = None

# Cheer sound duration (seconds)
CHEER_DURATION = 2.0


# ═══════════════════════════════════════════════
# MAIN MENU SCREEN
# ═══════════════════════════════════════════════
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        title = Label(
            text="Ahmed's World",
            font_size='32sp',
            bold=True,
            halign='center',
            size_hint=(1, 0.15)
        )
        layout.add_widget(title)

        btn_routine = Button(
            text="Bathroom Routine",
            font_size='22sp', bold=True,
            background_color=(0.2, 0.7, 0.9, 1),
            size_hint=(1, 0.2)
        )
        btn_routine.bind(on_press=lambda x: setattr(self.manager, 'current', 'toilet_routine'))
        layout.add_widget(btn_routine)

        btn_aac = Button(
            text="I Want",
            font_size='22sp', bold=True,
            background_color=(0.3, 0.8, 0.4, 1),
            size_hint=(1, 0.2)
        )
        btn_aac.bind(on_press=lambda x: setattr(self.manager, 'current', 'aac_board'))
        layout.add_widget(btn_aac)

        btn_quiz = Button(
            text="Quiz Game",
            font_size='22sp', bold=True,
            background_color=(0.9, 0.6, 0.2, 1),
            size_hint=(1, 0.2)
        )
        btn_quiz.bind(on_press=lambda x: setattr(self.manager, 'current', 'quiz_game'))
        layout.add_widget(btn_quiz)

        btn_memory = Button(
            text="Memory Game",
            font_size='22sp', bold=True,
            background_color=(0.7, 0.3, 0.8, 1),
            size_hint=(1, 0.2)
        )
        btn_memory.bind(on_press=lambda x: setattr(self.manager, 'current', 'memory_game'))
        layout.add_widget(btn_memory)

        self.add_widget(layout)


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
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text="Back",
            font_size='18sp',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=self.steps[0]["text"],
            font_size='26sp', bold=True,
            size_hint=(1, 0.12),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.img = Image(
            source=self.steps[0]["image"],
            size_hint=(1, 0.58),
            allow_stretch=True,
            keep_ratio=True,
            nocache=True
        )
        self.layout.add_widget(self.img)

        self.btn_next = Button(
            text="Done!",
            font_size='26sp',
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.2)
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
        Clock.schedule_once(lambda dt: self.play_step_audio(), 0.3)

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
        self.manager.current = 'main_menu'


# ═══════════════════════════════════════════════
# AAC BOARD SCREEN (I Want)
# ═══════════════════════════════════════════════
class AACBoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text="Back",
            font_size='18sp',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        main_layout.add_widget(btn_back)

        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.92))

        self.cards = [
            {"title": "I am Ahmed", "audio": "audio/say_ahmed.wav", "color": (0.2, 0.7, 0.9, 1)},
            {"title": "Dad Emad", "audio": "audio/say_dad.wav", "color": (0.3, 0.8, 0.4, 1)},
            {"title": "My Brother Mohamed", "audio": "audio/say_mohamed.wav", "color": (0.2, 0.8, 0.7, 1)},
            {"title": "My Brother Milad", "audio": "audio/say_milad.wav", "color": (0.9, 0.5, 0.7, 1)},
            {"title": "Water", "audio": "audio/say_water.wav", "color": (0.2, 0.6, 0.9, 1)},
            {"title": "Food", "audio": "audio/say_food.wav", "color": (1, 0.6, 0.2, 1)},
            {"title": "Bathroom", "audio": "audio/say_toilet.wav", "color": (0.4, 0.6, 0.8, 1)},
            {"title": "Sleep", "audio": "audio/say_sleep.wav", "color": (0.6, 0.4, 0.8, 1)},
            {"title": "Help", "audio": "audio/say_help.wav", "color": (0.9, 0.3, 0.3, 1)},
            {"title": "Play", "audio": "audio/say_play.wav", "color": (0.3, 0.8, 0.3, 1)},
            {"title": "Stop", "audio": "audio/say_stop.wav", "color": (0.8, 0.2, 0.2, 1)},
            {"title": "Happy", "audio": "audio/say_happy.wav", "color": (1, 0.4, 0.6, 1)}
        ]

        for card in self.cards:
            btn = Button(
                text=card["title"],
                font_size='20sp', bold=True,
                background_color=card["color"],
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda instance, a=card["audio"]: self.play_phrase(a))
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def play_phrase(self, audio_file):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        sound = SoundLoader.load(audio_file)
        if sound:
            self.current_sound = sound
            sound.play()


# ═══════════════════════════════════════════════
# QUIZ GAME SCREEN
# ═══════════════════════════════════════════════
class QuizGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None
        self.questions = [
            {
                "question": "Where is Ahmed?",
                "audio": "audio/q_ahmed.wav",
                "correct": "images/aac_ahmed.png",
                "options": ["images/aac_water.png", "images/aac_ahmed.png", "images/aac_food.png"]
            },
            {
                "question": "Where is Dad Emad?",
                "audio": "audio/q_dad.wav",
                "correct": "images/aac_dad.png",
                "options": ["images/aac_dad.png", "images/aac_play.png", "images/aac_toilet.png"]
            },
            {
                "question": "Where is Mohamed?",
                "audio": "audio/q_mohamed.wav",
                "correct": "images/aac_mohamed.png",
                "options": ["images/aac_milad.png", "images/aac_mohamed.png", "images/aac_ahmed.png"]
            },
            {
                "question": "Where is Milad?",
                "audio": "audio/q_milad.wav",
                "correct": "images/aac_milad.png",
                "options": ["images/aac_mohamed.png", "images/aac_food.png", "images/aac_milad.png"]
            }
        ]
        self.current_q = 0

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        btn_back = Button(
            text="Back",
            font_size='18sp',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=self.questions[0]["question"],
            font_size='26sp', bold=True,
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.77))
        self.update_options()
        self.layout.add_widget(self.grid)

        self.add_widget(self.layout)

    def on_enter(self):
        self.current_q = 0
        self.label.text = self.questions[0]["question"]
        self.update_options()
        Clock.schedule_once(lambda dt: self.play_q_audio(), 0.3)

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
        self.grid.clear_widgets()
        q_data = self.questions[self.current_q]
        for opt in q_data["options"]:
            btn = Button(
                background_normal='',
                background_color=(0.95, 0.95, 0.95, 1),
                size_hint=(1, 1)
            )
            img = Image(
                source=opt,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            btn.add_widget(img)
            btn.bind(on_press=lambda instance, i=opt: self.check_answer(i))
            self.grid.add_widget(btn)

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

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Top bar
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        btn_back = Button(
            text="Back",
            font_size='16sp',
            size_hint_x=0.3,
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        header.add_widget(btn_back)

        self.score_label = Label(
            text="Score: 0",
            font_size='18sp', bold=True,
            size_hint_x=0.4
        )
        header.add_widget(self.score_label)

        self.sound_btn = Button(
            text="Sound: ON",
            font_size='14sp',
            size_hint_x=0.3,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        self.sound_btn.bind(on_press=self.toggle_sound)
        header.add_widget(self.sound_btn)

        main_layout.add_widget(header)

        # 4x3 Card grid
        self.grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.8))
        main_layout.add_widget(self.grid)

        # Restart button
        restart_btn = Button(
            text="New Game",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp',
            bold=True
        )
        restart_btn.bind(on_press=lambda x: self.start_new_game())
        main_layout.add_widget(restart_btn)

        self.add_widget(main_layout)

    def on_enter(self):
        if not self.cards:
            self.start_new_game()

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

        # 6 matching pairs (1-6)
        card_values = list(range(1, 7)) * 2
        random.shuffle(card_values)

        for val in card_values:
            btn = Button(
                text="?",
                font_size='28sp',
                background_color=(0.3, 0.3, 0.3, 1)
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
                btn.background_color = (0.3, 0.3, 0.3, 1)
        self.selected_cards = []


# ═══════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════
class AhmedWorldApp(App):
    def build(self):
        self.title = "Ahmed's World"
        Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(ToiletRoutineScreen(name='toilet_routine'))
        sm.add_widget(AACBoardScreen(name='aac_board'))
        sm.add_widget(QuizGameScreen(name='quiz_game'))
        sm.add_widget(MemoryGameScreen(name='memory_game'))
        return sm

    def on_start(self):
        Window.clearcolor = (1, 1, 1, 1)


if __name__ == '__main__':
    AhmedWorldApp().run()
