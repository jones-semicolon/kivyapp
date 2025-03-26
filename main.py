from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.gridlayout import GridLayout
import random

USER_DATA = {"admin": "123"}


def get_sensor_data():
    """Simulate fetching sensor data"""
    return {
        "TDS": random.randint(800, 1500),
        "Nutrients": random.randint(1000, 2000),
        "pH": round(random.uniform(5.5, 7.5), 1),
        "Humidity": random.randint(60, 90),
        "Water Level": random.randint(20, 100),
    }


class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Responsive background rectangle
        with self.canvas.before:
            Color(0.29, 0.0, 0.51, 1)  # Dark Indigo Background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def create_centered_layout(self):
        scroll = ScrollView(size_hint=(1, 1))
        anchor = AnchorLayout(anchor_y="center")

        # Use a responsive width factor based on current window width
        width_factor = 0.9 if Window.width < 600 else 0.8
        layout = BoxLayout(
            orientation="vertical",
            padding=[Window.width * 0.01, Window.height * 0.02],  # dynamic padding
            spacing=Window.height * 0.02,  # dynamic spacing
            size_hint=(width_factor, None),
        )
        layout.bind(minimum_height=layout.setter("height"))

        anchor.add_widget(layout)
        scroll.add_widget(anchor)
        return scroll, layout


class SignupScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll, layout = self.create_centered_layout()

        # Responsive font sizes using Window.height as reference
        layout.add_widget(
            Label(
                text="Sign Up",
                font_size=sp(40),
                color=(0, 1, 1, 1),
                size_hint_y=None,
                height=dp(40),
            )
        )
        self.username_input = TextInput(
            hint_text="Username",
            size_hint_y=None,
            height=dp(40),
            padding=dp(10),
        )
        layout.add_widget(self.username_input)
        self.password_input = TextInput(
            hint_text="Password",
            size_hint_y=None,
            height=dp(40),
            padding=dp(10),
            password=True,
        )
        layout.add_widget(self.password_input)
        layout.add_widget(
            Button(
                text="Sign Up",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0, 1, 1, 1),
                on_press=self.signup,
            )
        )
        layout.add_widget(
            Button(
                text="Back to Login",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0, 1, 1, 1),
                on_press=self.go_to_login,
            )
        )

        self.add_widget(scroll)

    def signup(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            USER_DATA[username] = password
            Popup(
                title="Success",
                content=Label(text="Account created successfully!"),
                size_hint=(None, None),
                size=(300, 200),
            ).open()
            self.manager.current = "login"
        else:
            Popup(
                title="Error",
                content=Label(text="Please fill out both fields."),
                size_hint=(None, None),
                size=(300, 200),
            ).open()

    def go_to_login(self, instance):
        self.manager.current = "login"


class LoginScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll, layout = self.create_centered_layout()

        layout.add_widget(
            Label(
                text="Login",
                font_size=sp(40),
                color=(0, 1, 1, 1),
                size_hint_y=None,
                height=dp(40),
            )
        )
        self.username_input = TextInput(
            hint_text="Username", size_hint_y=None, height=dp(40), padding=dp(10)
        )
        layout.add_widget(self.username_input)
        self.password_input = TextInput(
            hint_text="Password",
            size_hint_y=None,
            height=dp(40),
            padding=dp(10),
            password=True,
        )
        layout.add_widget(self.password_input)
        layout.add_widget(
            Button(
                text="Login",
                size_hint_y=None,
                height=dp(40),
                background_color=(0, 1, 1, 1),
                on_press=self.login,
            )
        )
        layout.add_widget(
            Button(
                text="Sign Up",
                size_hint_y=None,
                height=dp(40),
                background_color=(0, 1, 1, 1),
                on_press=self.go_to_signup,
            )
        )

        self.add_widget(scroll)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username in USER_DATA and USER_DATA[username] == password:
            Popup(
                title="Success",
                content=Label(text="Login successful!"),
                size_hint=(None, None),
                size=(300, 200),
            ).open()
            self.manager.current = "user_agreement"
        else:
            Popup(
                title="Error",
                content=Label(text="Invalid credentials. Try again."),
                size_hint=(None, None),
                size=(300, 200),
            ).open()

    def go_to_signup(self, instance):
        self.manager.current = "signup"


class UserAgreementScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll, layout = self.create_centered_layout()

        layout.add_widget(
            Label(
                text="User Agreement",
                font_size=Window.height * 0.04,
                color=(0.0, 1.0, 1.0, 1),
                size_hint_y=None,
                height=dp(40),
            )
        )

        agreement_text = (
            "By continuing, you agree to the terms and conditions of this app. "
            "Please read them carefully."
        )

        # Horizontal layout for the checkbox and wrapped text
        checkbox_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(15), spacing=20
        )
        self.agree_checkbox = CheckBox(size_hint=(None, None), size=(30, 30))

        checkbox_text = Label(
            text=agreement_text,
            font_size=sp(10),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_x=None,
            width=Window.width * 0.7,  # Set width for wrapping
            text_size=(Window.width * 0.7, None),  # Enable text wrapping
            halign="left",
            valign="middle",
        )

        checkbox_layout.add_widget(self.agree_checkbox)
        checkbox_layout.add_widget(checkbox_text)

        layout.add_widget(checkbox_layout)

        layout.add_widget(
            Button(
                text="I Agree",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0.0, 1.0, 1.0, 1),
                on_press=self.confirm_agreement,
            )
        )
        self.add_widget(scroll)

    def confirm_agreement(self, instance):
        if self.agree_checkbox.active:
            Popup(
                title="Success",
                content=Label(text="Agreement confirmed! You can now proceed."),
                size_hint=(None, None),
                size=(300, 200),
            ).open()
            self.manager.current = "monitoring"
        else:
            Popup(
                title="Error",
                content=Label(text="You must agree to the terms to proceed."),
                size_hint=(None, None),
                size=(300, 200),
            ).open()


class MonitoringScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll, layout = self.create_centered_layout()

        layout.add_widget(
            Label(
                text="Hydroponics Monitoring",
                font_size=Window.height * 0.04,
                color=(0.0, 1.0, 1.0, 1),
                size_hint_y=None,
                height=dp(40),
            )
        )

        # Sensor data labels
        self.tds_label = Label(
            text="TDS Sensor: 1050 PPM",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )
        self.nutrients_label = Label(
            text="Nutrients: 1200 PPM",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )
        self.ph_label = Label(
            text="pH Level: 6.5",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )
        self.humidity_label = Label(
            text="Humidity: 85%",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )
        self.water_level_label = Label(
            text="Water Level: 50L",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )

        layout.add_widget(self.tds_label)
        layout.add_widget(self.nutrients_label)
        layout.add_widget(self.ph_label)
        layout.add_widget(self.humidity_label)
        layout.add_widget(self.water_level_label)

        # 2x3 GridLayout for sensor buttons
        self.sensor_buttons = GridLayout(
            cols=3, rows=2, size_hint_y=None, height=dp(180), spacing=dp(5)
        )
        layout.add_widget(self.sensor_buttons)

        # Create and add buttons
        buttons = [
            ("TDS Sensor", self.go_to_tds),
            ("Nutrients", self.go_to_nutrients),
            ("pH Level", self.go_to_ph),
            ("Humidity", self.go_to_humidity),
            ("Water Level", self.go_to_water_level),
            (
                "Other Sensor",
                self.go_to_other_sensor,
            ),  # Placeholder for an extra sensor
        ]

        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(None, None),
                size=(dp(90), dp(50)),  # Increased height for better text wrapping
                text_size=(dp(60), None),  # Allow text wrapping within button width
                halign="center",
                valign="middle",
                on_press=callback,
            )
            self.sensor_buttons.add_widget(btn)

        # Image processing button
        layout.add_widget(
            Button(
                text="Process Image",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0.0, 1.0, 1.0, 1),
                on_press=self.go_to_image_processing,
            )
        )

        self.add_widget(scroll)
        Clock.schedule_interval(self.update_sensor_data, 2)

    def update_sensor_data(self, dt):
        sensor_data = get_sensor_data()
        self.tds_label.text = f"TDS Sensor: {sensor_data['TDS']} PPM"
        self.nutrients_label.text = f"Nutrients: {sensor_data['Nutrients']} PPM"
        self.ph_label.text = f"pH Level: {sensor_data['pH']}"
        self.humidity_label.text = f"Humidity: {sensor_data['Humidity']}%"
        self.water_level_label.text = f"Water Level: {sensor_data['Water Level']}L"

    def go_to_tds(self, instance):
        self.manager.current = "tds"

    def go_to_nutrients(self, instance):
        self.manager.current = "nutrients"

    def go_to_ph(self, instance):
        self.manager.current = "ph"

    def go_to_humidity(self, instance):
        self.manager.current = "humidity"

    def go_to_water_level(self, instance):
        self.manager.current = "water_level"

    def go_to_other_sensor(self, instance):
        print("Other sensor clicked")  # Placeholder for additional functionality

    def go_to_image_processing(self, instance):
        self.manager.current = "image_processing"


class SensorPage(BaseScreen):

    def __init__(self, name, sensor_name, **kwargs):
        self.sensor_name = sensor_name
        super().__init__(name=name, **kwargs)
        scroll, layout = self.create_centered_layout()
        layout.add_widget(
            Label(
                text=sensor_name,
                font_size=Window.height * 0.04,
                color=(0.0, 1.0, 1.0, 1),
                size_hint_y=None,
                height=dp(40),
            )
        )

        sensor_data = get_sensor_data()
        sensor_value_label = Label(
            text=f"{sensor_name} Value: {sensor_data[sensor_name]}",
            font_size=Window.height * 0.03,
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30),
        )
        layout.add_widget(sensor_value_label)
        layout.add_widget(
            Button(
                text="Back to Monitoring",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0.0, 1.0, 1.0, 1),
                on_press=self.go_back,
            )
        )
        self.add_widget(scroll)

    def go_back(self, instance):
        self.manager.current = "monitoring"


class ImageProcessingScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll, layout = self.create_centered_layout()

        layout.add_widget(
            Label(
                text="Image Processing",
                font_size=Window.height * 0.04,
                color=(0.0, 1.0, 1.0, 1),
                size_hint_y=0.1,
            )
        )

        self.image = Image(size_hint=(1, 1))
        layout.add_widget(self.image)

        self.filechooser = FileChooserIconView(size_hint=(1, 0.6))
        layout.add_widget(self.filechooser)

        layout.add_widget(
            Button(
                text="Process Images",
                size_hint_y=None,
                height=dp(40),
                padding=dp(10),
                background_color=(0.0, 1.0, 1.0, 1),
                on_press=self.process_images,
            )
        )
        self.add_widget(scroll)

    def process_images(self, instance):
        selected_files = self.filechooser.selection
        if len(selected_files) < 5:
            Popup(
                title="Error",
                content=Label(text="Please select exactly 5 images."),
                size_hint=(None, None),
                size=(300, 200),
            ).open()
        else:
            self.image.source = selected_files[0]


# Main Screen Manager and App class
class ScreenManagement(ScreenManager):
    pass


class MyApp(App):

    def build(self):
        sm = ScreenManagement()
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(UserAgreementScreen(name="user_agreement"))
        sm.add_widget(MonitoringScreen(name="monitoring"))
        sm.add_widget(SensorPage(name="tds", sensor_name="TDS"))
        sm.add_widget(SensorPage(name="nutrients", sensor_name="Nutrients"))
        sm.add_widget(SensorPage(name="ph", sensor_name="pH"))
        sm.add_widget(SensorPage(name="humidity", sensor_name="Humidity"))
        sm.add_widget(SensorPage(name="water_level", sensor_name="Water Level"))
        sm.add_widget(ImageProcessingScreen(name="image_processing"))
        sm.current = "login"
        return sm


if __name__ == "__main__":
    MyApp().run()
