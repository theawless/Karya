import gi

gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Peas
from utilities.variables import PLUGIN_SEARCH_UI_PATH
from plugins.search.LocalSearch import LocalSearch
from plugins.search.OnlineSearch import OnlineSearch


class Search(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'SearchPlugin'
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        super().__init__()
        self.ui = Gtk.Builder.new_from_file(PLUGIN_SEARCH_UI_PATH)
        self.activator = None
        self.home_stack = None
        self.local_searcher = LocalSearch()
        self.online_searhcer = OnlineSearch()
        self.box = self.ui.get_object('SearchFullBox')
        self.menu_button = Gtk.Button()
        self.menu_button.set_image(Gtk.Image.new_from_icon_name('edit-find', Gtk.IconSize.SMALL_TOOLBAR))
        self.menu_button.connect('clicked', self.on_menu_button_click)

    def on_menu_button_click(self, widget):
        self.home_stack = self.activator.get_home_stack()
        self.home_stack.set_visible_child_name('search')

    def do_activate(self):
        print('search activated')
        self.activator.add_gui('search', 'Search', self.box, self.menu_button)
        self.box.show_all()
        self.menu_button.show_all()

    def do_deactivate(self):
        pass

    def get_activator(self, activator):
        print('search got activator')
        self.activator = activator
