import logging
import sys

import gi

from shell.windows import WindowLarge, WindowSmall
from utilities.dictation import DictationProvider

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio, GObject

from settings.mainsettings import WindowConfigurationHandler
from shell.windowelements import WindowModeSubscribers, WindowModes
from speech.speechrecogniser import SpeechRecogniser
from speech.dictator import Dictator
from shell.about import AboutPage

logger = logging.getLogger(__name__)


class Application(Gtk.Application, WindowModeSubscribers):
    __gsignals__ = {
        'mode_changed': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'settings_changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        Gtk.Application.__init__(self, flags=Gio.ApplicationFlags.FLAGS_NONE, )
        WindowModeSubscribers.__init__(self, None)
        GLib.set_application_name("Karya")
        GLib.set_prgname('karya')
        self.windowlarge = None
        self.windowsmall = None
        self.current_window = None

        self._window_settings_handler = WindowConfigurationHandler(self)
        self.speech_recogniser = SpeechRecogniser()
        self.dictator = Dictator(self.speech_recogniser)

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
        AboutPage(self.windowlarge)

    def quit(self, action, param):
        if self.windowlarge is not None:
            self.windowlarge.destroy()
        if self.windowsmall is not None:
            self.windowlarge.destroy()
        sys.exit()

    def do_activate(self):
        if not self.windowsmall:
            self.windowsmall = WindowSmall(self)
            self.windowsmall.speech_bar.mode_button.connect('clicked', self.mode_button_clicked)
            self.windowsmall.connect('delete-event', self.on_window_delete_event)
        if not self.windowlarge:
            self.windowlarge = WindowLarge(self)
            self.windowlarge.speech_bar.mode_button.connect('clicked', self.mode_button_clicked)
            self.windowlarge.connect('delete-event', self.on_window_delete_event)
        name = self._window_settings_handler.config['Main']['Window']
        if name == WindowModes.large.name:
            self.on_window_change(None, WindowModes.large)
        elif name == WindowModes.small.name:
            self.on_window_change(None, WindowModes.small)

    def on_window_delete_event(self, window, event):
        self.emit('settings_changed')
        self.quit(None, None)

    def mode_button_clicked(self, widget):
        # flip modes
        self.emit('settings_changed')
        if self.current_window.mode == WindowModes.large:
            self.on_window_change(None, WindowModes.small)
        elif self.current_window.mode == WindowModes.small:
            self.on_window_change(None, WindowModes.large)

    def setup_window(self):
        name = self.current_window.mode.name
        config = self._window_settings_handler.config
        size_x = config.getint(name, 'size_X')
        size_y = config.getint(name, 'size_Y')
        pos_x = config.getint(name, 'position_X')
        pos_y = config.getint(name, 'position_Y')
        self.current_window.resize_move(size_x, size_y, pos_x, pos_y)

    def on_window_change_large(self):
        self.current_window = self.windowlarge
        self.setup_window()
        self.windowlarge.show()
        self.windowsmall.hide()
        self.emit('mode_changed', self.windowlarge.mode)

    def on_window_change_small(self):
        self.current_window = self.windowsmall
        self.setup_window()
        self.windowlarge.hide()
        self.windowsmall.show()
        self.emit('mode_changed', self.windowsmall.mode)
