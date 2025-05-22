from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

scale_kv = """
AnchorLayout:
    id: arc_layout  
    size_hint: None, None
    width: root.width / 4
    height: self.width
    canvas.before:
        Color:
            rgba: root.color + [0.3]#root.bar_color + [0.3]
        Line:
            width: dp(3)#root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 180, 360 + 90)
    canvas.after:
        Color:
            rgb: root.color #root.bar_color + [0.3]
        Line:
            width: dp(3)#root.bar_width
            ellipse: (self.x, self.y, self.width, self.height, 180, ((root.value / root.max_value)  * 270) + 180)
    MDBoxLayout:
        orientation: "horizontal"
        adaptive_height: True
        adaptive_width: True
        size_hint: None, None 
        spacing: dp(2)
        MDLabel:
            id: value_label
            text: str(root.value) #"1040 PPM"
            theme_text_color: "Hint"
            size_hint_x: None
            adaptive_width: True
            valign: "center"
            font_size: "18sp"
        MDLabel:
            text: root.unit #"PPM"
            theme_text_color: "Hint"
            size_hint_x: None
            adaptive_width: True
            valign: "top"
            font_size: "8sp"
"""

status_kv = """
MDIcon:
    id: icon_widget
    icon: root.icon #"landslide"
    pos_hint: {"center_x": .5, "center_y": .5}
    font_size: dp(75) 
    theme_text_color: "Custom"
    text_color: root.color + ([1] if root.status else [0.1])
MDBoxLayout:
    orientation: "vertical"
    size_hint: 1, None
    adaptive_height: True
    MDLabel:
        text: root.text
        halign: "center"    
        size_hint_y: None
        height: self.texture_size[1] # Adjust height dynamically
        font_size: dp(12)
    MDLabel:
        text: root.description if root.description else ""
        size_hint_y: None
        height: self.texture_size[1] # Adjust height dynamically
        halign: "center"
        font_size: "9sp"
        disabled: True
"""


class SensorScreen(MDScreen):
    text = StringProperty("None")
    unit = StringProperty("None")
    value = NumericProperty(0)
    max_value = NumericProperty(1)
    min_value = NumericProperty(0)
    color = ListProperty([1, 1, 1])
    icon = StringProperty()
    status = BooleanProperty()

    def update_content(self):
        self.ids.card.clear_widgets()
        if self.icon:  # use `status_kv` if icon is set
            widget = Builder.load_string(status_kv)
        else:
            widget = Builder.load_string(scale_kv)
        self.ids.card.add_widget(widget)
