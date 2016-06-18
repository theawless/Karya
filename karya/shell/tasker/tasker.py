import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Tasker(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
