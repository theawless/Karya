import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Home(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.sidebar = Gtk.StackSidebar()
        self.stack = Gtk.Stack()
        self.sidebar.set_size_request(150,100)
        self.add(self.sidebar)
        self.pack_start(self.stack, True, True, 0)
        self.setup_stack()

    def setup_stack(self):
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.sidebar.set_stack(self.stack)
        self.add_to_stack('main', 'Updates', Gtk.Box())
        self.stack.show_all()
        self.sidebar.show_all()

    def add_to_stack(self, name, title, box):
        self.stack.add_titled(box, name, title)
