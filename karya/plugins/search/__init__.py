import os

import gi

gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Peas

PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
PLUGIN_SEARCH_UI_PATH = PLUGIN_PATH + '/ui/search.glade'

from .OnlineSearch import OnlineSearch
from .LocalSearch import LocalSearch
from .common import SearchCommon


class Search(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'SearchPlugins'
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        super().__init__()
        self.ui = Gtk.Builder.new_from_file(PLUGIN_SEARCH_UI_PATH)
        self.activator = None
        self.home_stack = None
        self.local_searcher = LocalSearch()
        self.online_searhcer = OnlineSearch()
        self.box = self.ui.get_object('SearchFullBox')
        self.tool_button = Gtk.ToolButton()
        self.tool_button.set_icon_widget(Gtk.Image.new_from_icon_name('edit-find', Gtk.IconSize.SMALL_TOOLBAR))
        self.tool_button.connect('clicked', self.on_menu_button_click)

    def on_menu_button_click(self, widget):
        self.home_stack = self.activator.get_home_stack()
        self.home_stack.set_visible_child_name('search')

    def do_activate(self):
        self.activator.add_gui('search', 'Search', self.box, self.tool_button)
        self.box.show_all()
        self.tool_button.show_all()
        SearchCommon(self.ui)

    def do_deactivate(self):
        pass

    def get_activator(self, activator):
        self.activator = activator
