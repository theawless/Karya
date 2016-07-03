import gi

from shell.windowelements import WindowModeSubscribers

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from shell.home import Home
from shell.tasker.tasker import Tasker


# maybe we will expand this class later
class View:
    def __init__(self):
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack = Gtk.Stack()
        self.home = Home()
        self.tasker = Tasker()
        self._setup_stack()

    def _setup_stack(self):
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.add_titled(self.home, 'home', 'Home')
        self.stack.add_titled(self.tasker, 'tasker', 'Tasker')
        self.stack_switcher.set_stack(self.stack)
        self.stack.show_all()
        self.stack_switcher.show_all()