import sys

import gi

from shell.about import AboutPage

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio
from shell.window import Window
import logging

logger = logging.getLogger(__name__)


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        GLib.set_application_name("Karya")
        GLib.set_prgname('karya')
        self._window = None

    def build_app_menu(self):
        action_entries = [
            ('about', self.about),
            ('help', self.help),
            ('quit', self.quit),
        ]

        menu = Gio.Menu()
        for action, callback in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)
            menu.append_item(Gio.MenuItem.new(action.title(), "app." + action))
        return menu

    def do_startup(self):
        Gtk.Application.do_startup(self)
        # else we have a fallback in window
        if self.prefers_app_menu():
            menu = self.build_app_menu()
            self.set_app_menu(menu)

    def help(self, action, param):
        logger.debug('help')

    def about(self, action, param):
        AboutPage(self._window)

    def quit(self, action, param):
        if self._window is not None:
            self._window.destroy()
        sys.exit()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
        # makes sure we have only one window open
        self._window.present()
