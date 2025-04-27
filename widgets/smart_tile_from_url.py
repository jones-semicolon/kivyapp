from kivymd.uix.imagelist import MDSmartTile
from kivy.uix.modalview import ModalView
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty


class FullScreenImage(ModalView):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.auto_dismiss = True
        self.add_widget(AsyncImage(source=source, allow_stretch=True, keep_ratio=True))


class SmartTileFromURL(MDSmartTile):
    source = StringProperty()

    def on_release(self):
        full_screen = FullScreenImage(source=self.source)
        full_screen.open()
