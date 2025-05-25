from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.lang import Builder
from widgets.sensor_widgets import SensorScale, SensorIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock


class SensorScreen(MDScreen):
    text = StringProperty("None")
    unit = StringProperty("None")
    value = NumericProperty(0)
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])
    icon = StringProperty()
    status = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.update_content)

    def update_content(self, dt=None):
        self.ids.card.clear_widgets()
        if self.icon:
            widget = SensorIcon(
                text=self.text, icon=self.icon, color=self.color, status=self.status
            )
        else:
            widget = SensorScale(
                text=self.text,
                unit=self.unit,
                value=self.value,
                max_value=self.max_value,
                color=self.color,
            )
        self.ids.card.add_widget(widget)
