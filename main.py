from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens import (
    LoginScreen,
    SignupScreen,
    TermsConditionsScreen,
    DashboardScreen,
    SensorScreen,
    IntroductionsScreen,
)
from kivy.storage.jsonstore import JsonStore


class MainApp(MDApp):
    def build(self):
        self.store = JsonStore("user_store.json")

        Builder.load_file("screens/kv/login_screen.kv")
        Builder.load_file("screens/kv/signup_screen.kv")
        Builder.load_file("screens/kv/terms_conditions.kv")
        Builder.load_file("screens/kv/dashboard.kv")
        Builder.load_file("widgets/kv/floating_window.kv")
        Builder.load_file("screens/kv/introductions.kv")
        Builder.load_file("widgets/kv/image.kv")
        Builder.load_file("widgets/kv/card.kv")

        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(TermsConditionsScreen(name="termsconditions"))
        sm.add_widget(SensorScreen(name="sensor"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(IntroductionsScreen(name="introductions"))
        self.theme_cls.theme_style = "Dark"

        return sm


if __name__ == "__main__":
    MainApp().run()
