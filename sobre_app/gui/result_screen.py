from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from core.alcohol_calc import courbe_alcoolemie, temps_retour_zero
from core.utils import format_duree

import datetime
import random

MESSAGES = [
    "Bravo, tu prends soin de toi !",
    "Encore un peu de patience...",
    "La route sera bientôt à toi !",
    "Reste hydraté et détends-toi !",
    "Tu es sur la bonne voie !",
    "Courage, la sobriété approche !",
    "Tu seras sobre dans {temps}, mais tu peux déjà commander un kebab. 🥙",
    "Sobre bientôt, mais l’eau c’est bien aussi ! 💧",
    "Encore {temps} avant d’être frais comme un gardon !"
]

class ResultScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', spacing=20, padding=40, pos_hint={'center_x':0.5, 'center_y':0.5})
        self.add_widget(self.layout)
        self.labels = {}
        self._build_ui()

    def _build_ui(self):
        card = MDCard(orientation='vertical', padding=30, size_hint=(None, None), size=(400, 400), pos_hint={'center_x':0.5, 'center_y':0.5})
        card.add_widget(MDIcon(icon='timer-sand', halign='center', theme_text_color='Custom', text_color=(1,0.7,0.2,1), font_size=72))
        self.labels['taux'] = MDLabel(text='Taux actuel : -- g/L', halign='center', font_style='H5')
        self.labels['heure'] = MDLabel(text='Heure de sobriété : --:--', halign='center', font_style='Subtitle1')
        self.labels['temps'] = MDLabel(text='Temps restant : --', halign='center', font_style='Subtitle1')
        self.labels['msg'] = MDLabel(text='', halign='center', font_style='Body1', theme_text_color='Secondary')
        for key in ['taux', 'heure', 'temps', 'msg']:
            card.add_widget(self.labels[key])
        self.recommencer_btn = MDRectangleFlatButton(text='Recommencer', pos_hint={'center_x':0.5}, font_size=22)
        self.recommencer_btn.bind(on_release=self._on_recommencer)
        card.add_widget(self.recommencer_btn)
        self.layout.add_widget(card)

    def afficher_resultat(self, profil, consommations, simulation_options=None):
        if not consommations:
            self.labels['taux'].text = 'Aucune consommation.'
            self.labels['heure'].text = ''
            self.labels['temps'].text = ''
            self.labels['msg'].text = random.choice(MESSAGES).format(temps='--')
            return
        poids = float(profil['poids'])
        sexe = profil['sexe']
        a_jeun = profil['a_jeun']
        heure_debut = min([int(c['heure'].split(':')[0])*60+int(c['heure'].split(':')[1]) for c in consommations])
        # Calcul du facteur métabolisme
        facteur = 1.0
        resume = []
        if simulation_options:
            if simulation_options.get('vite'):
                facteur -= 0.10
                resume.append('Bu vite (-10%)')
            if simulation_options.get('endormi'):
                facteur -= 0.20
                resume.append('Endormi (-20%)')
            if simulation_options.get('danse'):
                facteur += 0.10
                resume.append('Dansé (+10%)')
        # Passer le facteur au calcul
        points, pic, pic_time = courbe_alcoolemie(consommations, poids, sexe, a_jeun, heure_debut, taux_elimination=0.15*facteur)
        now = datetime.datetime.now()
        minute_now = now.hour*60 + now.minute
        taux_actuel = 0
        for minute, taux in points:
            if minute >= minute_now:
                taux_actuel = taux
                break
        minute_sobre = temps_retour_zero(points)
        heure_sobre = f"{minute_sobre//60:02d}:{minute_sobre%60:02d}"
        temps_restant = minute_sobre - minute_now
        temps_str = format_duree(temps_restant)
        self.labels['taux'].text = f"Taux actuel : {taux_actuel:.2f} g/L"
        self.labels['heure'].text = f"Heure de sobriété : {heure_sobre}"
        self.labels['temps'].text = f"Temps restant : {temps_str}"
        msg = random.choice(MESSAGES).format(temps=temps_str)
        if resume:
            msg += "\nFacteurs simulation : " + ", ".join(resume)
        self.labels['msg'].text = msg

    def _on_recommencer(self, instance):
        self.manager.current = 'home'
