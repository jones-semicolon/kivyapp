from kivymd.uix.card import MDCard
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior


class CustomCircularCard(MDCard, ButtonBehavior):
    text = StringProperty()
    unit = StringProperty()
    value = NumericProperty()
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])
    border = BooleanProperty(True)

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.on_border(self, self.border))

    def animate_value(self, new_value, duration=0.5):
        Animation.cancel_all(self, "value")
        anim = Animation(value=new_value, duration=duration, t="out_quad")
        anim.start(self)

    def on_click(self):
        app = App.get_running_app()
        screen_manager = app.root

        if not self.border:
            return

        sensor_screen = screen_manager.get_screen("sensor")
        sensor_screen.clear_wid()

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

    def on_border(self, instance, value):
        app = App.get_running_app()
        theme_cls = app.theme_cls

        if value:
            # Use themed background
            self.md_bg_color = (
                theme_cls.bg_light
                if theme_cls.theme_style == "Light"
                else theme_cls.bg_dark
            )
        else:
            # Transparent
            self.md_bg_color = (0, 0, 0, 0)


class CustomCard(MDCard, ButtonBehavior):
    text = StringProperty()
    icon = StringProperty()
    status = BooleanProperty()
    description = StringProperty()
    color = ListProperty([1, 1, 1])
    border = BooleanProperty(True)

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.on_border(self, self.border))

    def update_icon(self, new_icon):
        self.ids.icon_widget.icon = new_icon

    def update_value(self, new_value):
        self.status = new_value

    def on_click(self):
        app = App.get_running_app()
        screen_manager = app.root

        if not self.border:
            return

        sensor_screen = screen_manager.get_screen("sensor")
        sensor_screen.clear_wid()

        # Assign values to the target screen's properties
        sensor_screen.text = self.text
        sensor_screen.icon = self.icon
        sensor_screen.status = self.status
        sensor_screen.description = self.description
        sensor_screen.color = self.color

        sensor_screen.update_content()
        # Switch to the target screen
        screen_manager.current = "sensor"

    def on_border(self, instance, value):
        app = App.get_running_app()
        theme_cls = app.theme_cls

        if value:
            # Use themed background
            self.md_bg_color = (
                theme_cls.bg_light
                if theme_cls.theme_style == "Light"
                else theme_cls.bg_dark
            )
        else:
            # Transparent
            self.md_bg_color = (0, 0, 0, 0)
