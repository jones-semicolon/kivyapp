from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)


class SensorScreen(MDScreen):
    text = StringProperty()
    unit = StringProperty()
    value = None
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
