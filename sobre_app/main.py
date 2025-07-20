from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from gui.home_screen import HomeScreen
from gui.input_screen import InputScreen
from gui.result_screen import ResultScreen

class SobreakScreenManager(ScreenManager):
    pass

class SobreakApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # ou "Light" pour clair
        self.theme_cls.primary_palette = "BlueGray"
        sm = SobreakScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(InputScreen(name='input'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    SobreakApp().run()
