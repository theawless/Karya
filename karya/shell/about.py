import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from utilities.variables import ABOUT_UI_PATH


class AboutPage:
    def __init__(self, window):
        self.ui = Gtk.Builder()
        self.ui.add_from_file(ABOUT_UI_PATH)
        self.dialog = self.ui.get_object("AboutDialog")
        self._setup_dialog(window)

    def _setup_dialog(self, window):
        # to close in non gnome-desktops
        self.dialog.connect("response", self.on_about_dialog_close)
        self.dialog.set_transient_for(window)
        self.dialog.show_all()

    def on_about_dialog_close(self, dialog, response):
        self.dialog.destroy()
