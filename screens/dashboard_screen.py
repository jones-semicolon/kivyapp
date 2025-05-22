from datetime import datetime
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread, Clock
from kivy.network.urlrequest import UrlRequest
from widgets.custom_cards import CustomCard, CustomCircularCard
from widgets.floating_window import FloatingWindow
from kivy.lang import Builder
from constants import API_BASE_URL
from kivymd.uix.menu import MDDropdownMenu
from kivy.app import App


class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.floatingwindow = None
        self.data = None
        self.sensor_cards = {}
        self.light_cards = {}
        self.formatted_time = None

    def on_enter(self, *args):
        self.load_data()
        Clock.schedule_interval(lambda dt: self.load_data(), 10)

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
    def on_error(self, _, error):
        print("Failed to fetch data:", error)

    @mainthread
    def got_datas(self, _, result):
        if not result:
            print("No data provided.")
            return

        latest_entry, latest_time = None, None

        for entry in result:
            try:
                dt = datetime.strptime(entry.get("Time", ""), "%m/%d/%Y, %I:%M:%S %p")
                if latest_time is None or dt > latest_time:
                    latest_time = dt
                    latest_entry = entry
            except Exception:
                continue

        if not latest_entry:
            print("No valid entries.")
            return

        self.data = latest_entry
        if not self.sensor_cards:
            self.create_sensor_cards()
        else:
            self.update_sensor_cards()

    def create_sensor_cards(self):
        container = self.ids.container
        container.clear_widgets()

        # Initialize empty dicts to store cards
        self.sensor_cards = {}
        self.light_cards = {}
        self.pump_cards = {}

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
                "status": True,
                "description": f"Updated as of {self.formatted_time}",
                "status-icon": {
                    "on": "sprout",
                    "off": "lightbulb-off-outline",
                },
                "color": [0.694, 1, 0.694],
                "disabled": True,
            },
            {
                "icon": "lightbulb-on-outline",
                "text": "Grow Light",
                "key": "Grow Light Status",
                "status": str(self.data.get("Grow Light Status", "false")).lower()
                == "true",
                "description": "6:00 AM - 6:00 PM",
                "status-icon": {
                    "on": "lightbulb-on-outline",
                    "off": "lightbulb-off-outline",
                },
                "color": [1, 0.64, 0],
                "disabled": False,
            },
        ]

        for light in light_data:
            card = CustomCard(
                icon=light["icon"] if light["status"] else light["status-icon"]["off"],
                text=light["text"],
                status=light["status"],
                color=light["color"],
                description=light["description"],
                disabled=light["disabled"],
            )
            container.add_widget(card)
            self.light_cards[light["key"]] = card

        # Sensor cards
        sensor_data = [
            {
                "icon": "landslide",
                "text": "TDS",
                "key": "TDS",
                "value": float(self.data.get("TDS") or 0),
                "max_value": 1300,
                "unit": "PPM",
                "color": [0.8, 0.7, 0.5],
            },
            {
                "icon": "ph",
                "text": "pH Level",
                "key": "pH Level",
                "value": float(self.data.get("pH Level") or 0),
                "max_value": 7.0,
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

        pumps = [
            {
                "icon": "pump",
                "text": "Left Pump Status",
                "key": "Left Pump Status",
                "status": str(self.data.get("Left Pump Status", "false")).lower()
                == "true",
                "color": [1, 0.64, 0],
                "disabled": False,
            },
            {
                "icon": "pump",
                "text": "Right Pump Status",
                "key": "Right Pump Status",
                "status": str(self.data.get("Right Pump Status", "false")).lower()
                == "true",
                "color": [1, 0.64, 0],
                "disabled": False,
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

        for pump in pumps:
            card = CustomCard(
                icon=pump["icon"] if pump["status"] else "pump-off",
                text=pump["text"],
                status=pump["status"],
                color=pump["color"],
                disabled=pump["disabled"],
            )
            container.add_widget(card)
            self.pump_cards[pump["key"]] = card

    def update_sensor_cards(self):
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

        if "TDS" in self.sensor_cards:
            new_value = float(self.data.get("TDS") or 0)
            self.sensor_cards["TDS"].animate_value(new_value)

        # Update light cards (icon swap, no animation needed)
        if "Grow Light Status" in self.light_cards:
            new_value = self.data.get("Grow Light Status", False)

            # If new_value is string, fix it to boolean
            if isinstance(new_value, str):
                new_value = new_value.lower() == "true"

            card = self.light_cards["Grow Light Status"]

            card.update_value(new_value)

            # Update the icon manually
            if new_value:
                card.update_icon("lightbulb-on-outline")
            else:
                card.update_icon("lightbulb-off-outline")

        if "Right Pump Status" in self.pump_cards:
            new_value = self.data.get("Right Pump Status", False)

            # If new_value is string, fix it to boolean
            if isinstance(new_value, str):
                new_value = new_value.lower() == "true"

            card = self.pump_cards["Right Pump Status"]

            card.update_value(new_value)

            # Update the icon manually
            if new_value:
                card.update_icon("pump")
            else:
                card.update_icon("pump-off")

        if "Left Pump Status" in self.pump_cards:
            new_value = self.data.get("Left Pump Status", False)

            # If new_value is string, fix it to boolean
            if isinstance(new_value, str):
                new_value = new_value.lower() == "true"

            card = self.pump_cards["Left Pump Status"]

            card.update_value(new_value)

            # Update the icon manually
            if new_value:
                card.update_icon("pump")
            else:
                card.update_icon("pump-off")

        if "Status" in self.light_cards:
            status_card = self.light_cards["Status"]
            status_card.description = f"Updated as of {self.formatted_time}"

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
        app = App.get_running_app()
        if app.store.exists("user"):
            app.store.delete("user")
        self.manager.current = "login"
