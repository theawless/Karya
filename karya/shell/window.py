import gi

from shell.speechinfobar import SpeechInfoBar

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject
from utilities.pluginmanager import PluginManager
from utilities.activator import Activator
from settings.speechsettings import ConfigurableDialog

from shell.toolbar import Toolbar
from shell.view import View
from shell.windowelements import WindowModes, WindowElements


class Window(Gtk.ApplicationWindow, WindowElements):
    __gsignals__ = {
        'mode_changed': (GObject.SIGNAL_RUN_FIRST, None, (object,))
    }

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        # instead of window we send None, refer WindowElements
        WindowElements.__init__(self, None)
        self.set_size_request(800, 600)
        self.set_icon_name('karya')
        self.app = app
        self.window_box = Gtk.VBox()
        self.window_box.show()
        self.window_box.set_homogeneous(False)
        self.add(self.window_box)

        self.toolbar = Toolbar(self)
        self._setup_actions()
        self.set_titlebar(self.toolbar.header_bar)

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
        # first start is large window
        self.on_window_change(self, WindowModes.large)

    def response_info_bar(self, widget, response):
        if response == Gtk.ResponseType.CLOSE:
            self.app.quit(None, None)

    def mode_button_clicked(self, widget):
        # flip modes
        if self.window_mode == WindowModes.large:
            self.on_window_change(self, WindowModes.small)
        elif self.window_mode == WindowModes.small:
            self.on_window_change(self, WindowModes.large)

    def on_window_change_large(self):
        self.window_mode = WindowModes.large
        self.emit('mode-changed', self.window_mode)
        self.set_size_request(800, 600)
        self.resize(1, 1)

    def on_window_change_small(self):
        self.window_mode = WindowModes.small
        self.emit('mode-changed', self.window_mode)
        self.set_size_request(0, 0)
        self.resize(1, 1)

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
