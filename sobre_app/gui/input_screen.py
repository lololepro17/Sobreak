from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.widget import Widget
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.menu import MDDropdownMenu

class InputScreen(MDScreen):
    sexe = StringProperty('Homme')
    poids = StringProperty('')
    a_jeun = StringProperty('Non')
    consommations = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulation_options = {'vite': False, 'endormi': False, 'danse': False}
        self.poids = ''
        self.layout = MDBoxLayout(orientation='vertical', spacing=24, padding=20, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        scroll = MDScrollView()
        scroll.add_widget(self.layout)
        self.add_widget(scroll)
        # Titre général
        self.layout.add_widget(MDLabel(
            text='Nouvelle session',
            font_style='H4',
            halign='center',
            size_hint_y=None,
            height=64
        ))
        self.layout.add_widget(Widget(size_hint_y=None, height=16))
        self._build_profil()
        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self._build_simulation()
        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self._build_conso()
        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self._build_conso_list()
        self.layout.add_widget(Widget(size_hint_y=None, height=20))
        self._build_calculer_btn()

    def _build_profil(self):
        card = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), size_hint_y=None, md_bg_color=(0.18, 0.22, 0.28, 1))
        box = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(MDLabel(text='Profil utilisateur', font_style='H5', halign='center', size_hint_y=None, height=56, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(Widget(size_hint_y=None, height=8))
        # Sexe
        row_sexe = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_sexe.add_widget(MDLabel(text='Sexe :', font_style='Subtitle1', halign='right', size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.sexe_segment = MDSegmentedControl(size_hint_x=0.6, height=40)
        self.sexe_homme = MDSegmentedControlItem(text='Homme')
        self.sexe_femme = MDSegmentedControlItem(text='Femme')
        self.sexe_segment.add_widget(self.sexe_homme)
        self.sexe_segment.add_widget(self.sexe_femme)
        self.sexe_homme.active = True
        self.sexe_segment.bind(on_active=self._set_sexe)
        row_sexe.add_widget(self.sexe_segment)
        box.add_widget(row_sexe)
        # Poids
        row_poids = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_poids.add_widget(MDLabel(text='Poids (kg) :', font_style='Subtitle1', halign='right', size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.poids_input = MDTextField(input_filter='float', hint_text='Poids en kg', mode='rectangle', size_hint_x=0.6)
        self.poids_input.bind(text=lambda instance, value: setattr(self, 'poids', value))
        row_poids.add_widget(self.poids_input)
        box.add_widget(row_poids)
        # À jeun
        row_jeun = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_jeun.add_widget(MDLabel(text='À jeun :', font_style='Subtitle1', halign='right', size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.jeun_segment = MDSegmentedControl(size_hint_x=0.6, height=40)
        self.jeun_oui = MDSegmentedControlItem(text='Oui')
        self.jeun_non = MDSegmentedControlItem(text='Non')
        self.jeun_segment.add_widget(self.jeun_oui)
        self.jeun_segment.add_widget(self.jeun_non)
        self.jeun_non.active = True
        self.jeun_segment.bind(on_active=self._set_jeun)
        row_jeun.add_widget(self.jeun_segment)
        box.add_widget(row_jeun)
        card.add_widget(box)
        self.layout.add_widget(card)

    def _build_simulation(self):
        card = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), size_hint_y=None, md_bg_color=(0.28, 0.22, 0.18, 1))
        box = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(MDLabel(text='Mode Simulation', font_style='H5', halign='center', size_hint_y=None, height=56, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(Widget(size_hint_y=None, height=8))
        # Option 1
        row1 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        cb1 = MDCheckbox(active=False)
        cb1.bind(active=lambda instance, value: self._set_sim_option('vite', value))
        row1.add_widget(cb1)
        row1.add_widget(MDLabel(text="J’ai bu vite", halign='left', size_hint_x=1, size_hint_y=None, height=48, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(row1)
        # Option 2
        row2 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        cb2 = MDCheckbox(active=False)
        cb2.bind(active=lambda instance, value: self._set_sim_option('endormi', value))
        row2.add_widget(cb2)
        row2.add_widget(MDLabel(text="Je me suis endormi", halign='left', size_hint_x=1, size_hint_y=None, height=48, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(row2)
        # Option 3
        row3 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        cb3 = MDCheckbox(active=False)
        cb3.bind(active=lambda instance, value: self._set_sim_option('danse', value))
        row3.add_widget(cb3)
        row3.add_widget(MDLabel(text="J’ai dansé", halign='left', size_hint_x=1, size_hint_y=None, height=48, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(row3)
        card.add_widget(box)
        self.layout.add_widget(card)

    def _build_conso(self):
        card = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), size_hint_y=None, md_bg_color=(0.18, 0.28, 0.22, 1))
        box = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(MDLabel(text='Ajouter une consommation', font_style='H5', halign='center', size_hint_y=None, height=56, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(Widget(size_hint_y=None, height=8))
        # Type d'alcool
        row_type = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_type.add_widget(MDLabel(text="Type d'alcool", font_style="Subtitle1", size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.type_menu_items = [
            {"viewclass": "OneLineListItem", "text": t, "on_release": lambda x=t: self._set_type(x)}
            for t in ['Bière', 'Vin', 'Spiritueux']
        ]
        self.type_btn = MDRectangleFlatButton(text='Bière', on_release=self._open_type_menu, size_hint_x=0.5)
        self.type_menu = MDDropdownMenu(caller=self.type_btn, items=self.type_menu_items, width=200)
        row_type.add_widget(self.type_btn)
        box.add_widget(row_type)
        # Volume
        row_vol = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_vol.add_widget(MDLabel(text="Volume (cl)", font_style="Subtitle1", size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.volume_input = MDTextField(input_filter='float', hint_text='ex: 25', mode='rectangle', size_hint_x=0.5)
        row_vol.add_widget(self.volume_input)
        box.add_widget(row_vol)
        # Heure
        row_heure = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_heure.add_widget(MDLabel(text="Heure (HH:MM)", font_style="Subtitle1", size_hint_x=0.4, theme_text_color='Custom', text_color=(1,1,1,1)))
        self.heure_input = MDTextField(hint_text='ex: 22:30', mode='rectangle', size_hint_x=0.5)
        row_heure.add_widget(self.heure_input)
        box.add_widget(row_heure)
        # Bouton ajouter
        row_btn = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=48)
        row_btn.add_widget(MDLabel(size_hint_x=0.5))
        self.ajouter_btn = MDRaisedButton(
            text="Ajouter",
            md_bg_color=(0.2, 0.6, 1, 1),
            text_color=(1, 1, 1, 1),
            elevation=4,
            on_release=self._ajouter_conso
        )
        row_btn.add_widget(self.ajouter_btn)
        box.add_widget(row_btn)
        card.add_widget(box)
        self.layout.add_widget(card)

    def _build_conso_list(self):
        card = MDCard(orientation='vertical', padding=20, spacing=10, size_hint=(1, None), size_hint_y=None, md_bg_color=(0.22, 0.18, 0.28, 1))
        box = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        box.add_widget(MDLabel(text='Consommations', font_style='H5', halign='center', size_hint_y=None, height=56, theme_text_color='Custom', text_color=(1,1,1,1)))
        box.add_widget(Widget(size_hint_y=None, height=8))
        # Liste scrollable limitée en hauteur
        from kivymd.uix.list import OneLineListItem
        from kivymd.uix.scrollview import MDScrollView
        scroll = MDScrollView(size_hint=(1, None), height=200)
        self.liste_box = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.liste_box.bind(minimum_height=self.liste_box.setter('height'))
        scroll.add_widget(self.liste_box)
        box.add_widget(scroll)
        card.add_widget(box)
        self.layout.add_widget(card)

    def _refresh_conso_list(self, *args):
        self.liste_box.clear_widgets()
        if not self.consommations:
            self.liste_box.add_widget(MDLabel(text='Aucune consommation ajoutée.', halign='center', size_hint_y=None, height=40))
        else:
            for c in self.consommations:
                txt = f"{c['type']} - {c['volume']} cl à {c['heure']}"
                self.liste_box.add_widget(OneLineListItem(text=txt, size_hint_y=None, height=40))

    def _build_calculer_btn(self):
        from kivymd.uix.button import MDRaisedButton
        btn = MDRaisedButton(
            text='Calculer',
            md_bg_color=(0.2, 0.6, 1, 1),
            text_color=(1, 1, 1, 1),
            elevation=4,
            size_hint=(1, None),
            height=56,
            pos_hint={'center_x': 0.5},
            on_release=self._on_calculer
        )
        self.layout.add_widget(btn)

    def _set_sim_option(self, key, value):
        self.simulation_options[key] = value

    def _open_type_menu(self, instance):
        self.type_menu.open()
    def _set_type(self, type_):
        self.type_btn.text = type_
        self.type_menu.dismiss()

    def _set_sexe(self, instance, value):
        # instance est l'item activé, value est True/False
        if value and hasattr(instance, 'text'):
            self.sexe = instance.text

    def _set_jeun(self, instance, value):
        if value and hasattr(instance, 'text'):
            self.a_jeun = instance.text
    def _ajouter_conso(self, instance):
        type_ = self.type_btn.text
        volume = self.volume_input.text
        heure = self.heure_input.text
        if type_ and volume and heure:
            self.consommations.append({'type': type_, 'volume': volume, 'heure': heure})
            self.volume_input.text = ''
            self.heure_input.text = ''
            Clock.schedule_once(self._refresh_conso_list, 0.1)
    def _on_calculer(self, instance):
        profil = {
            'sexe': self.sexe,
            'poids': self.poids,
            'a_jeun': self.a_jeun
        }
        consommations = list(self.consommations)
        if not profil['poids'] or not consommations:
            from kivymd.toast import toast
            toast("Veuillez remplir le profil et ajouter au moins une consommation.")
            return
        try:
            result_screen = self.manager.get_screen('result')
        except Exception:
            from kivymd.toast import toast
            toast("Erreur : l'écran de résultats n'est pas disponible.")
            return
        result_screen.afficher_resultat(profil, consommations, self.simulation_options)
        self.manager.current = 'result'
