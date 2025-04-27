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
from datetime import datetime
from kivy.clock import Clock
from kivy.animation import Animation

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

    def animate_value(self, new_value, duration=0.5):
        Animation.cancel_all(self, "value")  # Cancel any previous animation
        anim = Animation(value=new_value, duration=duration, t="out_quad")
        anim.start(self)


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

    def update_icon(self, new_icon):
        self.ids.icon_widget.icon = new_icon  # or whatever your icon id is

    def update_value(self, new_value):
        self.value = new_value


class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.floatingwindow = None
        self.data = None  # No data yet
        self.sensor_data = []
        self.pumps = []
        self.light = []
        self.formatted_time = None

    def create_window(self):
        if not self.floatingwindow:
            self.floatingwindow = FloatingWindow()
            self.add_widget(self.floatingwindow, index=0)

    def on_enter(self, *args):
        self.load_data()
        Clock.schedule_interval(
            lambda dt: self.load_data(), 10
        )  # Reload every 10s       self.load_data()  # Load from server

    def load_data(self):
        url = f"{API_BASE_URL}/data/hydroponics"
        UrlRequest(
            url,
            on_success=self.got_datas,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,
            decode=True,
        )

    @mainthread
    def on_error(self, request, error):
        # handle network or parsing errors
        print("Failed to fetch images:", error)

    @mainthread
    def got_datas(self, request, result):
        if not result:
            print("No data provided.")
            return

        latest_entry = None
        latest_time = None

        for entry in result:
            time_str = entry.get("Time")
            if not time_str:
                continue
            try:
                dt = datetime.strptime(time_str, "%m/%d/%Y, %I:%M:%S %p")
            except (ValueError, TypeError):
                print(f"Skipping invalid time: {time_str}")
                continue

            if latest_time is None or dt > latest_time:
                latest_time = dt
                latest_entry = entry

        if latest_entry is None:
            print("No valid entries.")
            return

        self.data = latest_entry

        if not hasattr(self, "sensor_cards"):
            self.create_sensor_cards()  # first time create
        else:
            self.update_sensor_cards()  # afterwards just update

    def create_sensor_cards(self):
        container = self.ids.container
        container.clear_widgets()

        # Initialize empty dicts to store cards
        self.sensor_cards = {}
        self.light_cards = {}

        # Extract and format the time
        time_str = self.data.get("Time", "-")
        if time_str and time_str != "-":
            try:
                dt = datetime.strptime(time_str, "%m/%d/%Y, %I:%M:%S %p")
                self.formatted_time = dt.strftime(
                    "%I:%M %p"
                )  # Only the hour:minute AM/PM
            except Exception:
                self.formatted_time = "-"
        else:
            self.formatted_time = "-"

        # Light cards
        light_data = [
            {
                "icon": "sprout",
                "text": "Status",
                "key": "Status",
                "value": True,
                "description": f"Updated as of {self.formatted_time}",
                "status-icon": {
                    "on": "sprout",
                    "off": "lightbulb-off-outline",
                },
                "color": [0.694, 1, 0.694],
            },
            {
                "icon": "lightbulb-on-outline",
                "text": "Grow Light",
                "key": "Grow Light Status",
                "value": str(self.data.get("Grow Light Status", "false")).lower()
                == "true",
                "description": "6:00 AM - 6:00 PM",
                "status-icon": {
                    "on": "lightbulb-on-outline",
                    "off": "lightbulb-off-outline",
                },
                "color": [1, 0.64, 0],
            },
        ]

        for light in light_data:
            card = CustomCard(
                icon=light["icon"] if light["value"] else light["status-icon"]["off"],
                text=light["text"],
                value=light["value"],
                color=light["color"],
                description=light["description"],
            )
            container.add_widget(card)
            self.light_cards[light["key"]] = card

        # Sensor cards
        sensor_data = [
            {
                "icon": "landslide",
                "text": "TDS",
                "key": "TDS",
                "value": 720,  # No dynamic data yet
                "max_value": 1040,
                "unit": "PPM",
                "color": [0.8, 0.7, 0.5],
            },
            {
                "icon": "ph",
                "text": "pH Level",
                "key": "pH Level",
                "value": float(self.data.get("pH Level") or 0),
                "max_value": 7.5,
                "unit": "pH",
                "color": [0.31373, 0.78431, 0.47059],
            },
            {
                "icon": "weather-windy",
                "text": "Humidity",
                "key": "Humidity",
                "value": float(self.data.get("Humidity") or 0),
                "max_value": 100,
                "unit": "%",
                "color": [0, 0.74, 1],
            },
            {
                "icon": "waves-arrow-up",
                "text": "Water Level",
                "key": "Water Level",
                "value": float(self.data.get("Water Level") or 0),
                "max_value": 100,
                "unit": "L",
                "color": [0.11, 0.56, 0.8],
            },
        ]

        for sensor in sensor_data:
            card = CustomCircularCard(
                text=sensor["text"],
                value=sensor["value"],
                max_value=sensor["max_value"],
                unit=sensor["unit"],
                color=sensor["color"],
            )
            container.add_widget(card)
            self.sensor_cards[sensor["key"]] = card

    def update_sensor_cards(self):
        # Update sensor cards
        time_str = self.data.get("Time", "-")
        if time_str and time_str != "-":
            try:
                dt = datetime.strptime(time_str, "%m/%d/%Y, %I:%M:%S %p")
                self.formatted_time = dt.strftime("%I:%M %p")
            except Exception:
                self.formatted_time = "-"
        else:
            self.formatted_time = "-"

        if "pH Level" in self.sensor_cards:
            new_value = float(self.data.get("pH Level") or 0)
            self.sensor_cards["pH Level"].animate_value(new_value)

        if "Humidity" in self.sensor_cards:
            new_value = float(self.data.get("Humidity") or 0)
            self.sensor_cards["Humidity"].animate_value(new_value)

        if "Water Level" in self.sensor_cards:
            new_value = float(self.data.get("Water Level") or 0)
            self.sensor_cards["Water Level"].animate_value(new_value)

        # Update light cards (icon swap, no animation needed)
        if "Grow Light Status" in self.light_cards:
            new_value = self.data.get("Grow Light Status", False)

            # If new_value is string, fix it to boolean
            if isinstance(new_value, str):
                new_value = new_value.lower() == "true"

            card = self.light_cards["Grow Light Status"]  # <-- you missed this line

            card.update_value(new_value)

            # Update the icon manually
            if new_value:
                card.update_icon("lightbulb-on-outline")
            else:
                card.update_icon("lightbulb-off-outline")

        if "Status" in self.light_cards:
            status_card = self.light_cards["Status"]
            status_card.description = (
                f"Updated as of {self.formatted_time}"  # <-- use formatted_time here
            )


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
