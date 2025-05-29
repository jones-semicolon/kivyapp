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
        self.images_by_folder = None

    def load_images(self):
        url = f"{API_BASE_URL}/images/{FOLDER_ID}"
        UrlRequest(
            url,
            on_success=self.got_images,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=30,
            decode=True,
        )

    @mainthread
    def got_images(self, _, result):
        # Ensure imagesByFolder is a dictionary, not a list
        self.images_by_folder = result.get("imagesByFolder", {})
        self.clear_layout()

    def image_list(self, folderName):
        if not folderName:
            return

        self.ids.grid.clear_widgets()
        self.ids.list.clear_widgets()
        self.ids.back.disabled = False
        self.ids.back.opacity = 1

        # Retrieve the list of files for the selected folder
        files = self.images_by_folder.get(folderName, [])

        for file in files:
            tile = SmartTileFromURL(source=file["downloadUrl"])
            self.ids.grid.add_widget(tile)

    def clear_layout(self):
        self.ids.grid.clear_widgets()
        self.ids.list.clear_widgets()
        self.ids.back.disabled = True
        self.ids.back.opacity = 0

        for folderName in self.images_by_folder:
            # Create a button for each folder
            folder_button = MDRaisedButton(text=str(folderName), size_hint=(1, 1))
            # Bind the on_release event using a lambda to capture folderName
            folder_button.bind(
                on_release=lambda instance, fname=folderName: self.image_list(fname)
            )
            self.ids.list.add_widget(folder_button)

    @mainthread
    def on_error(self, _, error):
        print("Failed to fetch images:", error)

    def close_window(self):
        if self.parent:
            self.parent.floatingwindow = None
            self.parent.remove_widget(self)
