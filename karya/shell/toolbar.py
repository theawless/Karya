import gi

from shell.windowelements import WindowElements

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


# contains header bar and later (possibly) search bar
class Toolbar(WindowElements):
    def __init__(self, window):
        super().__init__(window)
        self.header_bar = Gtk.HeaderBar()
        self._setup_header_bar()
        self._setup_header_menu()

    def _setup_header_bar(self):
        self.header_bar.set_title('Karya')
        self.header_bar.set_show_close_button(True)
        self.header_bar.show_all()

    # actions handled by window
    def _setup_header_menu(self):
        menu_button = Gtk.MenuButton()
        menu_button.set_image(Gtk.Image.new_from_icon_name('preferences-system', Gtk.IconSize.SMALL_TOOLBAR))
        menu = Gio.Menu()
        plugin_item = Gio.MenuItem.new('Plugins', 'win.plugins')
        settings_item = Gio.MenuItem.new('Settings', 'win.settings')
        menu.append_item(plugin_item)
        menu.append_item(settings_item)

        popover = Gtk.Popover()
        popover.bind_model(menu)
        menu_button.set_popover(popover)
        menu_button.show_all()
        self.header_bar.pack_end(menu_button)

    def build_alternate_app_menu(self, app):
        menu_button = Gtk.MenuButton()
        menu_button.set_image(Gtk.Image.new_from_icon_name('karya', Gtk.IconSize.SMALL_TOOLBAR))
        menu = app.build_app_menu()
        popover = Gtk.Popover()
        popover.bind_model(menu)
        menu_button.set_popover(popover)
        menu_button.show_all()
        self.header_bar.pack_start(menu_button)

    def on_window_change_small(self):
        self.header_bar.hide()

    def on_window_change_large(self):
        self.header_bar.show()
