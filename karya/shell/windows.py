import gi

from shell.speechinfobar import SpeechInfoBar
from shell.windowelements import WindowModes

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from utilities.pluginmanager import PluginManager
from utilities.activator import Activator
from settings.speechsettings import SpeechConfigurableDialog
from shell.toolbars import ToolbarLarge, ToolbarSmall
from shell.view import View

import logging

logger = logging.getLogger(__name__)


class WindowLarge(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        self.set_icon_name('karya')
        self.mode = WindowModes.large
        self.toolbar = ToolbarLarge()
        self._setup_actions()
        self.set_titlebar(self.toolbar.header_bar)
        self.speech_recogniser = app.speech_recogniser
        # to provide alternate fallback if build app menu failed
        self.set_show_menubar(False)
        if not app.prefers_app_menu():
            self.toolbar.build_alternate_app_menu(app)

        window_box = Gtk.VBox()
        window_box.show()
        window_box.set_homogeneous(False)
        self.add(window_box)

        self.view = View()
        self.toolbar.header_bar.set_custom_title(self.view.stack_switcher)
        window_box.pack_start(self.view.stack, True, True, 0)

        self.speech_bar = SpeechInfoBar(self.speech_recogniser)
        window_box.pack_start(self.speech_bar.info_bar, False, False, 0)

        self.activator = Activator(app, self, self.view.home, self.speech_recogniser)
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
            SpeechConfigurableDialog(self)
        else:
            logging.debug('window menu unknown')

    def add_plugin_menu_box(self, plugin_menu_box):
        self.toolbar.header_bar.pack_end(plugin_menu_box)

    def resize_move(self, size_x, size_y, pos_x, pos_y):
        self.resize(size_x, size_y)
        self.move(pos_x, pos_y)


class WindowSmall(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Karya")
        self.set_icon_name('karya')
        self.app = app
        self.mode = WindowModes.small
        self.set_show_menubar(False)
        self.set_keep_above(True)
        self.set_deletable(False)
        self.header_bar = ToolbarSmall(self.app.speech_recogniser)
        self.speech_bar = self.header_bar
        self.set_titlebar(self.header_bar.header_bar)
        self.speech_bar.info_bar.connect('response', self.on_speech_info_bar_response)

    def on_speech_info_bar_response(self, infobar, response):
        if response == Gtk.ResponseType.CLOSE:
            self.close()

    def resize_move(self, size_x, size_y, pos_x, pos_y):
        self.resize(size_x, size_y)
        self.move(pos_x, pos_y)
