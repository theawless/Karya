import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from utilities.pluginmanager import PluginManager
from utilities.activator import Activator
from settings.speechsettings import ConfigurableDialog

from shell.toolbar import Toolbar
from shell.view import View


class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        self.set_size_request(800, 600)
        self.set_icon_name('karya')
        self.app = app

        self.toolbar = Toolbar()
        self._setup_actions()
        self.set_titlebar(self.toolbar.header_bar)

        self.view = View()
        self.toolbar.header_bar.set_custom_title(self.view.stack_switcher)
        self.add(self.view.stack)

        self.activator = Activator(self.app, self, self.view.home, self.app.speech_recogniser)
        self.plugin_manager = PluginManager(self.activator)

    # gui buttons are created by toolbar
    def _setup_actions(self):
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

    def add_plugin_menu_box(self, plugin_menu_box):
        self.toolbar.header_bar.pack_end(plugin_menu_box)
