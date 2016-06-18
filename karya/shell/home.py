import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Home(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.sidebar = Gtk.StackSidebar()
        self.stack = Gtk.Stack()
        self.add(self.sidebar)
        self.add(self.stack)
        self.setup_stack()

    def setup_stack(self):
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.sidebar.set_stack(self.stack)
        self.add_to_stack('Hello World', 'Hello', Gtk.Box())
        self.stack.show_all()
        self.sidebar.show_all()

    def add_to_stack(self, name, title, box):
        self.stack.add_titled(box, name, title)
