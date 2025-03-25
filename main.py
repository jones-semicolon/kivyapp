from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
import random
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle

# Dummy storage for user data (replace with real database in production)
USER_DATA = {}


def get_sensor_data():
    """Simulate fetching sensor data"""
    return {
        "TDS": random.randint(800, 1500),
        "Nutrients": random.randint(1000, 2000),
        "pH": round(random.uniform(5.5, 7.5), 1),
        "Humidity": random.randint(60, 90),
        "Water Level": random.randint(20, 100),
    }


class DarkIndigoBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.2, 0.6, 1)  # Dark indigo color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(text="Sign Up", font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None, height=40)
        layout.add_widget(label)

        self.username_input = TextInput(hint_text="Username", size_hint_y=None, height=40)
        layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Password", size_hint_y=None, height=40, password=True)
        layout.add_widget(self.password_input)

        signup_button = Button(text="Sign Up", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                               on_press=self.signup)
        layout.add_widget(signup_button)

        back_button = Button(text="Back to Login", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                             on_press=self.go_to_login)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def signup(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            USER_DATA[username] = password
            popup = Popup(title="Success", content=Label(text="Account created successfully!"), size_hint=(None, None),
                          size=(300, 200))
            popup.open()
            self.manager.current = 'login'
        else:
            popup = Popup(title="Error", content=Label(text="Please fill out both fields."), size_hint=(None, None),
                          size=(300, 200))
            popup.open()

    def go_to_login(self, instance):
        self.manager.current = 'login'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(text="Login", font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None, height=40)
        layout.add_widget(label)

        self.username_input = TextInput(hint_text="Username", size_hint_y=None, height=40)
        layout.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Password", size_hint_y=None, height=40, password=True)
        layout.add_widget(self.password_input)

        login_button = Button(text="Login", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                              on_press=self.login)
        layout.add_widget(login_button)

        signup_button = Button(text="Sign Up", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                               on_press=self.go_to_signup)
        layout.add_widget(signup_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if username in USER_DATA and USER_DATA[username] == password:
            popup = Popup(title="Success", content=Label(text="Login successful!"), size_hint=(None, None),
                          size=(300, 200))
            popup.open()
            self.manager.current = 'user_agreement'
        else:
            popup = Popup(title="Error", content=Label(text="Invalid credentials. Try again."), size_hint=(None, None),
                          size=(300, 200))
            popup.open()

    def go_to_signup(self, instance):
        self.manager.current = 'signup'


class UserAgreementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)
        label = Label(text="User Agreement", font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None, height=40)
        layout.add_widget(label)

        agreement_text = """
        By continuing, you agree to the terms and conditions of this app. 
        Please read them carefully.
        """
        terms_label = Label(text=agreement_text, font_size=18, size_hint_y=None, height=200, color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(terms_label)

        self.agree_checkbox = CheckBox(size_hint=(None, None), size=(30, 30), color=(0.0, 1.0, 1.0, 1))
        layout.add_widget(self.agree_checkbox)

        agree_button = Button(text="I Agree", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                              on_press=self.confirm_agreement)
        layout.add_widget(agree_button)

        self.add_widget(layout)

    def confirm_agreement(self, instance):
        if self.agree_checkbox.active:
            popup = Popup(title="Success", content=Label(text="Agreement confirmed! You can now proceed."), size_hint=(None, None), size=(300, 200))
            popup.open()
            self.manager.current = 'monitoring'
        else:
            popup = Popup(title="Error", content=Label(text="You must agree to the terms to proceed."), size_hint=(None, None), size=(300, 200))
            popup.open()


class MonitoringScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)

        sensor_label = Label(text="Hydroponics Monitoring", font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None,
                             height=40)
        layout.add_widget(sensor_label)

        self.tds_label = Label(text="TDS Sensor: 1050 PPM", font_size=18, size_hint_y=None, height=40,
                               color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.tds_label)

        self.nutrients_label = Label(text="Nutrients: 1200 PPM", font_size=18, size_hint_y=None, height=40,
                                     color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.nutrients_label)

        self.ph_label = Label(text="pH Level: 6.5", font_size=18, size_hint_y=None, height=40, color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.ph_label)

        self.humidity_label = Label(text="Humidity: 85%", font_size=18, size_hint_y=None, height=40,
                                    color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.humidity_label)

        self.water_level_label = Label(text="Water Level: 50L", font_size=18, size_hint_y=None, height=40,
                                       color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(self.water_level_label)

        self.sensor_buttons = BoxLayout(size_hint_y=None, height=50)
        layout.add_widget(self.sensor_buttons)

        image_processing_button = Button(text="Process Image", size_hint_y=None, height=50,
                                         background_color=(0.0, 1.0, 1.0, 1), on_press=self.go_to_image_processing)
        layout.add_widget(image_processing_button)

        self.add_widget(layout)

        Clock.schedule_interval(self.update_sensor_data, 2)

    def update_sensor_data(self, dt):
        sensor_data = get_sensor_data()

        self.tds_label.text = f"TDS Sensor: {sensor_data['TDS']} PPM"
        self.nutrients_label.text = f"Nutrients: {sensor_data['Nutrients']} PPM"
        self.ph_label.text = f"pH Level: {sensor_data['pH']}"
        self.humidity_label.text = f"Humidity: {sensor_data['Humidity']}%"
        self.water_level_label.text = f"Water Level: {sensor_data['Water Level']}L"

        self.sensor_buttons.clear_widgets()
        self.sensor_buttons.add_widget(Button(text="TDS Sensor", on_press=self.go_to_tds))
        self.sensor_buttons.add_widget(Button(text="Nutrients", on_press=self.go_to_nutrients))
        self.sensor_buttons.add_widget(Button(text="pH Level", on_press=self.go_to_ph))
        self.sensor_buttons.add_widget(Button(text="Humidity", on_press=self.go_to_humidity))
        self.sensor_buttons.add_widget(Button(text="Water Level", on_press=self.go_to_water_level))

    def go_to_tds(self, instance):
        self.manager.current = 'tds'

    def go_to_nutrients(self, instance):
        self.manager.current = 'nutrients'

    def go_to_ph(self, instance):
        self.manager.current = 'ph'

    def go_to_humidity(self, instance):
        self.manager.current = 'humidity'

    def go_to_water_level(self, instance):
        self.manager.current = 'water_level'

    def go_to_image_processing(self, instance):
        self.manager.current = 'image_processing'


class SensorPage(Screen):
    def __init__(self, sensor_name, **kwargs):
        super().__init__(**kwargs)
        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(text=sensor_name, font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None, height=40)
        layout.add_widget(label)

        sensor_data = get_sensor_data()

        sensor_value_label = Label(text=f"{sensor_name} Value: {sensor_data[sensor_name]}", font_size=18,
                                   size_hint_y=None, height=40, color=(0.7, 0.7, 0.7, 1))
        layout.add_widget(sensor_value_label)

        back_button = Button(text="Back to Monitoring", size_hint_y=None, height=50,
                             background_color=(0.0, 1.0, 1.0, 1), on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'monitoring'


class ImageProcessingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = DarkIndigoBoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(text="Image Processing", font_size=30, color=(0.0, 1.0, 1.0, 1), size_hint_y=None, height=40)
        layout.add_widget(label)

        self.image = Image(size_hint=(1, 1))
        layout.add_widget(self.image)

        self.filechooser = FileChooserIconView(size_hint=(1, 0.6))
        layout.add_widget(self.filechooser)

        process_button = Button(text="Process Images", size_hint_y=None, height=50, background_color=(0.0, 1.0, 1.0, 1),
                                on_press=self.process_images)
        layout.add_widget(process_button)

        self.add_widget(layout)

    def process_images(self, instance):
        selected_files = self.filechooser.selection
        if len(selected_files) < 5:
            popup = Popup(title="Error", content=Label(text="Please select exactly 5 images."), size_hint=(None, None),
                          size=(300, 200))
            popup.open()
        else:
            self.image.source = selected_files[0]


class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        sm = ScreenManagement()

        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(UserAgreementScreen(name='user_agreement'))
        sm.add_widget(MonitoringScreen(name='monitoring'))
        sm.add_widget(SensorPage(name='tds', sensor_name="TDS"))
        sm.add_widget(SensorPage(name='nutrients', sensor_name="Nutrients"))
        sm.add_widget(SensorPage(name='ph', sensor_name="pH"))
        sm.add_widget(SensorPage(name='humidity', sensor_name="Humidity"))
        sm.add_widget(SensorPage(name='water_level', sensor_name="Water Level"))
        sm.add_widget(ImageProcessingScreen(name='image_processing'))

        sm.current = 'login'

        return sm


if __name__ == '__main__':
    MyApp().run()
