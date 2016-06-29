import gi

from settings.mainsettings import WindowConfigurationHandler
from shell.speechinfobar import SpeechInfoBar

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, Gdk
from utilities.pluginmanager import PluginManager
from utilities.activator import Activator
from settings.speechsettings import SpeechConfigurableDialog
from shell.toolbar import Toolbar
from shell.view import View
from shell.windowelements import WindowModes, WindowElements

import logging

logger = logging.getLogger(__name__)


class Window(Gtk.ApplicationWindow, WindowElements):
    __gsignals__ = {
        'mode_changed': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'settings_changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        # instead of window we send None, refer WindowElements
        WindowElements.__init__(self, None)
        self.set_icon_name('karya')
        self.app = app

        self.toolbar = Toolbar(self)
        self._setup_actions()
        self.set_titlebar(self.toolbar.header_bar)

        # to provide alternate fallback if build app menu failed
        self.set_show_menubar(False)
        if not self.app.prefers_app_menu():
            self.toolbar.build_alternate_app_menu(self.app)

        self.set_gravity(Gdk.Gravity.CENTER)
        self.window_box = Gtk.VBox()
        self.window_box.show()
        self.window_box.set_homogeneous(False)
        self.add(self.window_box)

        self.speech_info_bar = SpeechInfoBar(self)
        self.window_box.pack_start(self.speech_info_bar.info_bar, False, False, 0)
        self.speech_info_bar.info_bar.connect('response', self.response_info_bar)
        self.speech_info_bar.mode_button.connect('clicked', self.mode_button_clicked)

        self.view = View(self)
        self.toolbar.header_bar.set_custom_title(self.view.stack_switcher)
        self.window_box.pack_start(self.view.stack, True, True, 0)

        self.activator = Activator(self.app, self, self.view.home, self.speech_info_bar.speech_recogniser)
        self.plugin_manager = PluginManager(self.activator)

        self.window_mode = None

        self.settings_handler = WindowConfigurationHandler(self)
        self.settings_handler.connect('settings_loaded', self.on_settings_loaded)
        self.settings_handler.load_settings()
        self.connect('delete-event', self.on_window_delete_event)

    def on_window_delete_event(self, window, event):
        self.emit('settings_changed')

    def response_info_bar(self, widget, response):
        self.emit('settings_changed')
        if response == Gtk.ResponseType.CLOSE:
            self.app.quit(None, None)

    def mode_button_clicked(self, widget):
        # flip modes and save settings of current mode
        self.emit('settings_changed')
        if self.window_mode == WindowModes.large:
            self.on_window_change(self, WindowModes.small)
        elif self.window_mode == WindowModes.small:
            self.on_window_change(self, WindowModes.large)

    def on_settings_loaded(self, settings_handler, config):
        name = config['Main']['Window']
        window_mode = None
        if name == WindowModes.large.name:
            window_mode = WindowModes.large
        elif name == WindowModes.small.name:
            window_mode = WindowModes.small
        self.on_window_change(self, window_mode)

    def change_window_mode(self, mode, size_x, size_y, pos_x, pos_y):
        self.window_mode = mode
        self.emit('mode-changed', mode)
        self.resize(size_x, size_y)
        self.move(pos_x, pos_y)

    def on_window_change_large(self):
        config = self.settings_handler.config
        mode = WindowModes.large
        name = mode.name
        self.change_window_mode(mode, config.getint(name, 'size_X'), config.getint(name, 'size_Y'),
                                config.getint(name, 'position_X'), config.getint(name, 'position_Y')
                                )

    def on_window_change_small(self):
        config = self.settings_handler.config
        mode = WindowModes.small
        name = mode.name
        self.change_window_mode(mode,
                                config.getint(name, 'size_X'), config.getint(name, 'size_Y'),
                                config.getint(name, 'position_X'), config.getint(name, 'position_Y')
                                )

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
            SpeechConfigurableDialog(self)
        else:
            logging.debug('window menu unknown')

    def add_plugin_menu_box(self, plugin_menu_box):
        self.toolbar.header_bar.pack_end(plugin_menu_box)
