import sys

import gi

gi.require_version('PeasGtk', '1.0')
gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio
from shell.window import Window
from shell.about import AboutPage
from utilities.pluginmanager import PluginManager


class Application(Gtk.Application):
    # constructor for the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)
        GLib.set_application_name("Karya")
        GLib.set_prgname('karya')
        self.plugin_manager = PluginManager()
        self._window = None

    def build_app_menu(self):
        action_entries = [
            ('about', self.about),
            ('settings', self.configure),
            ('plugins', self.plugins),
            ('help', self.help),
            ('quit', self.quit),
        ]
        menu = Gio.Menu()
        for action, callback in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            menu.append_item(Gio.MenuItem.new(action.title(), "app." + action))
        self.set_app_menu(menu)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.build_app_menu()

    def plugins(self, action, param):
        self.plugin_manager.add_gui(self._window)

    def help(self, action, param):
        pass

    def about(self, action, param):
        AboutPage(self._window)

    def configure(self, action, param):
        pass

    def quit(self, action, param):
        self._window.destroy()
        sys.exit()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
        # makes sure we have only one window open
        self._window.present()
