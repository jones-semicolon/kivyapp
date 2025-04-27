from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivy.clock import mainthread
from constants import API_BASE_URL
from kivy.network.urlrequest import UrlRequest
import json


class SignupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.load_data()  # Load user data when the screen initializes

    def load_data(self):
        # URL to fetch data from the API (optional, can be used to check for existing users)
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

    def signup(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if username and password:
            # Check if the username already exists in self.data
            if any(user["username"] == username for user in self.data):
                self.dialog = MDDialog(
                    title="Error",
                    text="Username already exists. Please choose a different one.",
                    buttons=[
                        MDRaisedButton(
                            text="OK", on_release=lambda _: self.dialog.dismiss()
                        )
                    ],
                )
                self.dialog.open()
                return  # Prevent further signup if username exists

            # Proceed with signup if the username is unique
            user_data = {
                "username": username,
                "password": password,  # Send plain text password to the server
            }

            # Convert the dictionary to a JSON string
            body = json.dumps(user_data)

            # URL to send the POST request to
            url = f"{API_BASE_URL}/user"

            headers = {
                "Content-Type": "application/json",  # Set the content type to JSON
            }

            # Sending JSON as a string in the req_body argument
            UrlRequest(
                url,
                method="POST",
                req_body=body,  # Use req_body for the request body
                req_headers=headers,
                on_success=self.on_signup_success,
                on_error=self.on_error,
                on_failure=self.on_error,
                timeout=10,
                decode=True,
            )
        else:
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

    @mainthread
    def on_signup_success(self, _, result):
        # Check if the message field contains 'Data saved'
        if result.get("message") == "Data saved":
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
            self.manager.current = (
                "login"  # Switch to login screen after successful signup
            )
        else:
            self.dialog = MDDialog(
                title="Error",
                text="Failed to create account. Please try again.",
                buttons=[
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
            self.dialog.open()
