from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.uix.image import AsyncImage
from kivy.uix.modalview import ModalView
from kivymd.uix.menu import MDDropdownMenu
from kivy.network.urlrequest import UrlRequest
from kivy.clock import mainthread

# Load KV files manually
Builder.load_file("login_screen.kv")
Builder.load_file("signup_screen.kv")
Builder.load_file("terms_conditions.kv")
Builder.load_file("dashboard.kv")
Builder.load_file("card.kv")
Builder.load_file("floating_window.kv")
Builder.load_file("image.kv")

USER_DATA = {"admin": "123"}
API_BASE_URL = "https://kivyapp-production.up.railway.app"
folder_id = "1LQx5LpcYfqhfQHZYrcTbOPMsOzhz9q9F"


class TermsConditionsScreen(MDScreen):
    pass


class FullScreenImage(ModalView):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.auto_dismiss = True  # Closes on tap outside the image
        # Use AsyncImage if you want to load remote images
        self.add_widget(AsyncImage(source=source, allow_stretch=True, keep_ratio=True))


class SmartTileFromURL(MDSmartTile):
    # Ensure that you have a source property defined
    source = StringProperty()

    def on_release(self):
        # Open the full-screen modal with the image
        full_screen = FullScreenImage(source=self.source)
        full_screen.open()


class FloatingWindow(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_images()

    def load_images(self):
        url = f"{API_BASE_URL}/images/{folder_id}"
        # Kick off the GET request; when it succeeds, `got_images` is called
        UrlRequest(
            url,
            on_success=self.got_images,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,
            decode=True,
        )

    @mainthread
    def got_images(self, request, result):
        """
        result will be the parsed JSON:
          { "images": [ { "id": "...", "name": "...", "downloadUrl": "..." }, … ] }
        """
        for file in result.get("images", []):
            tile = SmartTileFromURL(source=file["downloadUrl"])
            self.ids.grid.add_widget(tile)

    @mainthread
    def on_error(self, request, error):
        # handle network or parsing errors
        print("Failed to fetch images:", error)

    def close_window(self):
        if self.parent:
            self.parent.floatingwindow = None
            self.parent.remove_widget(self)


class CustomCircularCard(MDCard):
    text = StringProperty()
    unit = StringProperty()
    value = NumericProperty()
    max_value = NumericProperty(1)
    color = ListProperty([1, 1, 1])

    def __init__(
        self,
        text="",
        value=0,
        unit="PPM",
        max_value=1,
        color=[],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.unit = unit
        self.value = value
        self.max_value = float(max_value)
        self.color = color


class CustomCard(MDCard):
    text = StringProperty()
    icon = StringProperty()
    value = BooleanProperty()
    description = StringProperty()
    color = ListProperty([1, 1, 1])

    def __init__(
        self,
        text="",
        value=False,
        icon="",
        description="",
        color=[],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.icon = icon
        self.value = value
        self.color = color
        self.description = description


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
            "color": [0.8, 0.7, 0.5],
        },
        {
            "icon": "ph",
            "text": "pH Level",
            "value": 1.2,
            "max_value": 7.5,
            "unit": "pH",
            "color": [0.31373, 0.78431, 0.47059],
        },
        {
            "icon": "weather-windy",
            "text": "Humidity",
            "value": 69,
            "max_value": 100,
            "unit": "%",
            "color": [0, 0.74, 1],
        },
        {
            "icon": "waves-arrow-up",
            "text": "Water Level",
            "value": 89,
            "max_value": 100,
            "unit": "L",
            "color": [0.11, 0.56, 0.8],
        },
    ]
    pumps = [
        {
            "icon": "pump",
            "text": "Left Pump",
            "value": False,
            "color": [1, 0.64, 0],
        },
        {
            "icon": "pump",
            "text": "Right Pump",
            "value": True,
            "color": [1, 0.64, 0],
        },
    ]
    light = {
        "icon": "lightbulb-on-outline",
        "text": "Grow Light",
        "description": "6:00 AM - 6:00 PM",
        "value": False,
        "color": [1, 0.64, 0],
    }

    def create_sensor_cards(self):
        container = self.ids.container
        full_container = self.ids.full_container
        full_card = CustomCard(
            icon=self.light["icon"] if self.light["value"] else "lightbulb-off-outline",
            text=self.light["text"],
            description=self.light["description"],
            value=self.light["value"],
            color=self.light["color"],
        )
        full_container.add_widget(full_card)
        for sensor in self.sensor_data:
            card = CustomCircularCard(
                text=sensor["text"],
                value=sensor["value"],
                max_value=sensor["max_value"],
                unit=sensor["unit"],
                color=sensor["color"],
            )
            container.add_widget(card)
        for pumps in self.pumps:
            card = CustomCard(
                icon=pumps["icon"] if pumps["value"] else "pump-off",
                text=pumps["text"],
                value=pumps["value"],
                color=pumps["color"],
            )
            container.add_widget(card)
        # circularCard = CustomCircularCard(
        #     text=self.sensor_data["text"],
        #     value=self.sensor_data["value"],
        #     max_value=self.sensor_data["max_value"],
        #     unit=self.sensor_data["unit"],
        #     color=self.sensor_data["color"],
        # )
        # container.add_widget(circularCard)

    def create_window(self):
        if not self.floatingwindow:
            self.floatingwindow = FloatingWindow()
            self.add_widget(self.floatingwindow, index=0)

    def open_menu(self, caller):
        menu_items = [
            {
                "text": "Logout",
                "viewclass": "OneLineListItem",
                "on_release": self.logout,
            }
        ]
        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            hor_growth="left",  # This makes menu grow to the left
            position="bottom",  # Position below the caller
            width_mult=0,
            width="32dp",
        )
        self.menu.open()

    def logout(self):
        print("Logging out...")
        self.menu.dismiss()
        self.manager.current = "login"


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
