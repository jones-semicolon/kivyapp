from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.lang import Builder
from widgets.custom_cards import CustomCard, CustomCircularCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock


class SensorScreen(MDScreen):
    text = StringProperty("None")
    unit = StringProperty("None")
    value = NumericProperty(0)
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])
    icon = StringProperty("")
    status = BooleanProperty("")
    description = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_content(self):
        self.ids.card.clear_widgets()
        if self.icon and self.icon.strip():
            widget = CustomCard(
                text=self.text,
                icon=self.icon,
                color=self.color,
                status=self.status,
                ripple_behavior=False,
                description=self.description,
                border=False,
            )
        else:
            widget = CustomCircularCard(
                text=self.text,
                unit=self.unit,
                value=self.value,
                max_value=self.max_value,
                color=self.color,
                ripple_behavior=False,
                border=False,
            )
        self.ids.card.add_widget(widget)
        self.clear_wid()

    def clear_wid(self):
        self.text = ""
        self.unit = ""
        self.value = 0
        self.max_value = 0
        self.min_value = 0
        self.color = [1, 1, 1]
        self.icon = ""
        self.status = ""
