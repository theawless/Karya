import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from shell.home import Home
from shell.tasker.tasker import Tasker
from utilities.pluginmanager import PluginManager
from utilities.activator import Activator
from settings.settings import ConfigurableDialog


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        self.set_size_request(800, 600)
        self.set_icon_name('karya')

        self.header_bar = Gtk.HeaderBar()
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack = Gtk.Stack()
        self.home = Home()
        self.Tasker = Tasker()
        self.setup_stack()
        self.setup_header_menu()
        self.setup_header_bar()

        self.activator = Activator(app, self, self.home, None)
        self.plugin_manager = PluginManager(self.activator)

    def setup_stack(self):
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.add_titled(self.home, 'home', 'Home')
        self.stack.add_titled(self.Tasker, 'tasker', 'Tasker')
        self.stack_switcher.set_stack(self.stack)
        self.header_bar.set_custom_title(self.stack_switcher)
        self.add(self.stack)
        self.stack.show_all()
        self.stack_switcher.show_all()

    def setup_header_menu(self):
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

        plugins_action = Gio.SimpleAction(name='plugins')
        plugins_action.connect('activate', self.cb_menu, 'plugins')
        self.add_action(plugins_action)
        settings_action = Gio.SimpleAction(name='settings')
        settings_action.connect('activate', self.cb_menu, 'settings')
        self.add_action(settings_action)

    def cb_menu(self, action, user, user_data):
        if user_data == 'plugins':
            self.plugin_manager.add_gui(self)
        elif user_data == 'settings':
            print('settings')
            ConfigurableDialog(self)
        else:
            print('window menu unknown')

    def setup_header_bar(self):
        self.header_bar.set_title('Karya')
        self.header_bar.set_show_close_button(True)
        self.set_titlebar(self.header_bar)
        self.header_bar.show_all()

    def add_plugin_menu_box(self, plugin_menu_box):
        self.header_bar.pack_end(plugin_menu_box)
