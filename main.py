from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens import LoginScreen, SignupScreen, TermsConditionsScreen, DashboardScreen


class MainApp(MDApp):

    def build(self):
        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(TermsConditionsScreen(name="termsconditions"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        # sm.current = "dashboard"
        self.theme_cls.theme_style = "Dark"
        return sm


if __name__ == "__main__":
    MainApp().run()
