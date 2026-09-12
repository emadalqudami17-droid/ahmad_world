import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.utils import platform

# Safe import for vibrator via plyer
try:
    from plyer import vibrator
except Exception:
    vibrator = None


class MemoryGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.score = 0
        self.sound_enabled = True

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        # Top Info Bar
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.score_label = Label(text="Score: 0", font_size='20sp', bold=True)
        self.sound_btn = Button(text="Sound: ON", size_hint_x=0.4, on_press=self.toggle_sound)
        header.add_widget(self.score_label)
        header.add_widget(self.sound_btn)
        self.add_widget(header)

        # Card Grid (4x3)
        self.grid = GridLayout(cols=4, spacing=5, size_hint_y=0.8)
        self.add_widget(self.grid)

        # Restart Game Button
        restart_btn = Button(
            text="New Game",
            size_hint_y=0.1,
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp',
            bold=True,
            on_press=lambda x: self.start_new_game()
        )
        self.add_widget(restart_btn)

    def toggle_sound(self, instance):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.text = "Sound: ON" if self.sound_enabled else "Sound: OFF"

    def play_sound(self, sound_file):
        if self.sound_enabled:
            if os.path.exists(sound_file):
                sound = SoundLoader.load(sound_file)
                if sound:
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

        # Generate 6 matching pairs
        card_values = list(range(1, 7)) * 2
        random.shuffle(card_values)

        for val in card_values:
            btn = Button(
                text="?",
                font_size='24sp',
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
            
            # Match sound from your audio assets
            self.play_sound("audio1.wav")
            self.trigger_vibration(0.1)
            self.selected_cards = []

            if self.matched_pairs == 6:
                self.score_label.text = f"Victory! Total Score: {self.score}"
                # Win sound from your audio assets
                self.play_sound("cheer.wav")
        else:
            self.score = max(0, self.score - 2)
            self.score_label.text = f"Score: {self.score}"
            from kivy.clock import Clock
            Clock.schedule_once(self.reset_selected, 0.8)

    def reset_selected(self, dt):
        for btn in self.selected_cards:
            if not btn.is_matched:
                btn.text = "?"
                btn.background_color = (0.3, 0.3, 0.3, 1)
        self.selected_cards = []


class MemoryApp(App):
    def build(self):
        self.title = "Ahmed's World"
        return MemoryGame()


if __name__ == '__main__':
    MemoryApp().run()
