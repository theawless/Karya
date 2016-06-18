import gi

gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Peas


class Search(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'ExamplePlugin'
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        super().__init__()
        self.activator = None

    def on_menu_button_click(self, widget):
        pass

    def do_activate(self):
        print('activated example plugin')
        pass

    def do_deactivate(self):
        pass

    def get_activator(self, activator):
        self.activator = activator
