from kivymd.uix.card import MDCard
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.animation import Animation


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


class CustomCard(MDCard):
    text = StringProperty()
    icon = StringProperty()
    value = BooleanProperty()
    description = StringProperty()
    color = ListProperty([1, 1, 1])

    def update_icon(self, new_icon):
        self.ids.icon_widget.icon = new_icon

    def update_value(self, new_value):
        self.value = new_value
