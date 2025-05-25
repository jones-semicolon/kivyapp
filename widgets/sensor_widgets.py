from kivymd.uix.anchorlayout import AnchorLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.app import App


class SensorScale(AnchorLayout):
    text = StringProperty()
    unit = StringProperty()
    value = NumericProperty()
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])


class SensorIcon(AnchorLayout):
    text = StringProperty()
    icon = StringProperty()
    status = BooleanProperty()
    description = StringProperty()
    color = ListProperty([1, 1, 1])
