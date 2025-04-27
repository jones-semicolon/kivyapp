from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.clock import mainthread, Clock
from constants import API_BASE_URL
from kivy.network.urlrequest import UrlRequest
from passlib.hash import (
    bcrypt,
)  # Use passlib's bcrypt hashing for password verification


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.load_data()  # Load user data when the screen initializes

    def load_data(self):
        # URL to fetch data from the API
        url = f"{API_BASE_URL}/user"
        UrlRequest(
            url,
            on_success=self.on_success,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,
            decode=True,
        )

    @mainthread
    def on_success(self, _, result):
        if not result:
            print("No data provided.")
            return
        self.data = result  # Store data from the API

    @mainthread
    def on_error(self, _, error):
        print("Failed to fetch data:", error)

    def dismiss(self):
        self.dialog.dismiss()
        self.manager.current = "termsconditions"

    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if self.data:  # Ensure data is available
            # Check if the username exists in the data
            user = next(
                (user for user in self.data if user["username"] == username), None
            )

            if user and bcrypt.verify(
                password, user["password"]
            ):  # Verify password hash
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
                self.dialog.open()
        else:
            self.dialog = MDDialog(
                title="Error",
                text="User data not loaded yet",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
            self.dialog.open()
