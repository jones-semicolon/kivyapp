from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty

# Load KV files manually
Builder.load_file("login_screen.kv")
Builder.load_file("signup_screen.kv")
Builder.load_file("terms_conditions.kv")
Builder.load_file("dashboard.kv")
Builder.load_file("card.kv")
Builder.load_file("floating_window.kv")

USER_DATA = {"admin": "123"}


class TermsConditionsScreen(MDScreen):
    pass


class FloatingWindow(MDFloatLayout):
    pass


class CustomCard(MDCard):
    text = StringProperty()
    icon = StringProperty()
    unit = StringProperty()
    value = NumericProperty()
    max_value = NumericProperty(1)
    color = ListProperty([1, 1, 1, 1])
    light_color = ListProperty([1, 1, 1, 1])

    def __init__(
        self,
        text="",
        icon="",
        value=0,
        unit="PPM",
        max_value=1,
        color=[],
        light_color=[],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.icon = icon
        self.unit = unit
        self.value = value
        self.max_value = float(max_value)
        self.color = color
        self.light_color = [min(1, c + 0.4) for c in color[:3]] + [
            0.3
        ]  # Make it lighter


class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_sensor_cards()
        self.floatingwindow = None

    sensor_data = [
        {
            "icon": "landslide",
            "text": "TDS",
            "value": 720,
            "max_value": 1040,
            "unit": "PPM",
            "color": [0.8, 0.7, 0.5, 1],
        },
        # {
        #     "icon": "lightbulb-on-outline",
        #     "text": "Grow Light",
        #     "value": 520,
        #     "max_value": 1040,
        #     "unit": "PPM",
        #     "color": [1, 0.64, 0, 1],
        # },
        {
            "icon": "ph",
            "text": "pH Level",
            "value": 6.9,
            "max_value": 14,
            "unit": "pH",
            "color": [0.31373, 0.78431, 0.47059, 1],
        },
        {
            "icon": "weather-windy",
            "text": "Humidity",
            "value": 69,
            "max_value": 100,
            "unit": "%",
            "color": [0, 0.74, 1, 1],
        },
        {
            "icon": "waves-arrow-up",
            "text": "Water Level",
            "value": 69,
            "max_value": 200,
            "unit": "L",
            "color": [0.11, 0.56, 0.8, 1],
        },
    ]

    def create_sensor_cards(self):
        container = self.ids.container
        for sensor in self.sensor_data:
            card = CustomCard(
                text=sensor["text"],
                icon=sensor["icon"],
                value=sensor["value"],
                max_value=sensor["max_value"],
                unit=sensor["unit"],
                color=sensor["color"],
            )
            container.add_widget(card)

    def create_window(self):
        if not self.floatingwindow:
            self.floatingwindow = FloatingWindow()
            self.add_widget(self.floatingwindow, index=0)


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dismiss(self):
        self.dialog.dismiss()
        self.manager.current = "termsconditions"  # Change to the actual home screen

    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if username in USER_DATA and USER_DATA[username] == password:
            self.dialog = MDDialog(
                title="Success",
                text="Login Successfully",
                buttons=[
                    MDRaisedButton(text="OK", on_release=lambda _: self.dismiss())
                ],
            )
            self.dialog.open()

        else:
            self.dialog = MDDialog(
                title="Error",
                text="Invalid Credentials",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
            self.dialog.open()  # <-- Add this to show the error popup


class SignupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def signup(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if username and password:
            USER_DATA[username] = password  # Ensure USER_DATA is a dictionary

            # Success Dialog
            self.dialog = MDDialog(
                title="Success",
                text="Account Created Successfully",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
            self.dialog.open()
            self.manager.current = "login"

        else:
            # Error Dialog
            self.dialog = MDDialog(
                title="Error",
                text="Please fill out both fields.",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
            self.dialog.open()
