import gi

gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Peas, Gdk


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        self.set_size_request(200, 100)
        self.set_icon_name('karya')

