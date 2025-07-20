from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel, MDIcon

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=30, padding=40, pos_hint={'center_x':0.5, 'center_y':0.5})
        layout.add_widget(MDIcon(icon='glass-cocktail', halign='center', theme_text_color='Custom', text_color=(0.2,0.6,1,1), font_size=96))
        layout.add_widget(MDLabel(text='Bienvenue sur Sobreak !', halign='center', font_style='H4'))
        btn = MDRectangleFlatButton(text='Commencer', pos_hint={'center_x':0.5}, font_size=24)
        btn.bind(on_press=self.go_to_input)
        layout.add_widget(btn)
        self.add_widget(layout)

    def go_to_input(self, instance):
        self.manager.current = 'input'
