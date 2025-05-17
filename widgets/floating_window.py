from kivymd.uix.floatlayout import MDFloatLayout
from kivy.network.urlrequest import UrlRequest
from kivy.clock import mainthread
from kivymd.uix.button import MDRaisedButton
from widgets.smart_tile_from_url import SmartTileFromURL
from constants import API_BASE_URL, FOLDER_ID


class FloatingWindow(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_images()

    def load_images(self):
        url = f"{API_BASE_URL}/images/{FOLDER_ID}"
        UrlRequest(
            url,
            on_success=self.got_images,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,
            decode=True,
        )

    @mainthread
    def got_images(self, _, result):
        # Ensure imagesByFolder is a dictionary, not a list
        images_by_folder = result.get("imagesByFolder", {})

        for folderName in images_by_folder.items():
            # Create a button for each folder
            folder_button = MDRaisedButton(text=str(folderName))
            self.ids.grid.add_widget(folder_button)

            # # Add each file in the folder
            # for file in files:
            #     tile = SmartTileFromURL(source=file["downloadUrl"])
            #     self.ids.grid.add_widget(tile)

    @mainthread
    def on_error(self, _, error):
        print("Failed to fetch images:", error)

    def close_window(self):
        if self.parent:
            self.parent.floatingwindow = None
            self.parent.remove_widget(self)
