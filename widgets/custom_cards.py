from kivymd.uix.card import MDCard
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.animation import Animation
from kivy.app import App


class CustomCircularCard(MDCard):
    text = StringProperty()
    unit = StringProperty()
    value = NumericProperty()
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])

    def animate_value(self, new_value, duration=0.5):
        Animation.cancel_all(self, "value")
        anim = Animation(value=new_value, duration=duration, t="out_quad")
        anim.start(self)

    def on_click(self):
        app = App.get_running_app()
        screen_manager = app.root

        sensor_screen = screen_manager.get_screen("sensor")

        # Assign values to the target screen's properties
        sensor_screen.text = self.text
        sensor_screen.unit = self.unit
        sensor_screen.value = self.value
        sensor_screen.max_value = self.max_value
        sensor_screen.min_value = self.min_value
        sensor_screen.color = self.color

        sensor_screen.update_content()
        # Switch to the target screen
        screen_manager.current = "sensor"


class CustomCard(MDCard):
    text = StringProperty()
    icon = StringProperty()
    status = BooleanProperty()
    description = StringProperty()
    color = ListProperty([1, 1, 1])
    disabled = BooleanProperty(True)

    def update_icon(self, new_icon):
        self.ids.icon_widget.icon = new_icon

    def update_value(self, new_value):
        self.status = new_value

    def on_click(self):
        app = App.get_running_app()
        screen_manager = app.root

        sensor_screen = screen_manager.get_screen("sensor")

        # Assign values to the target screen's properties
        sensor_screen.text = self.text
        sensor_screen.icon = self.icon
        sensor_screen.status = self.status
        sensor_screen.description = self.description
        sensor_screen.color = self.color
        sensor_screen.disabled = self.disabled

        sensor_screen.update_content()
        # Switch to the target screen
        screen_manager.current = "sensor"
