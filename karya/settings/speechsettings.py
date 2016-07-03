import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from settings.mainsettings import ConfigurationHandler
from utilities.variables import SPEECH_SETTINGS_UI_PATH, SPEECH_INI_PATH


class SpeechSettingsHandler(ConfigurationHandler):
    # a static variable in all instances

    # acting like multiple constructors
    def __init__(self, obj=None):
        super().__init__(obj, SPEECH_INI_PATH)
        self.load_settings()

    def default_settings(self):
        self.config['Main'] = {'recogniser': 'WITAI', 'dynamic_noise_suppression': 'False'}
        self.config['Sphinx'] = {'version': 'pocketsphinx'}
        self.config['Google'] = {'api_key': ''}
        self.config['WITAI'] = {'api_key': ''}
        self.config['APIAI'] = {'api_key': ''}
        self.config['Bing'] = {'api_key': ''}
        self.config['IBM'] = {'username': '', 'password': ''}
        return self.config

    def save_settings(self, obj):
        if self.obj.ui.get_object("sphinx_radio").get_active():
            self.config['Main']['recogniser'] = "Sphinx"
        elif self.obj.ui.get_object("google_radio").get_active():
            self.config['Main']['recogniser'] = "Google"
        elif self.obj.ui.get_object("witai_radio").get_active():
            self.config['Main']['recogniser'] = "WITAI"
        elif self.obj.ui.get_object("ibm_radio").get_active():
            self.config['Main']['recogniser'] = "IBM"
        elif self.obj.ui.get_object("apiai_radio").get_active():
            self.config['Main']['recogniser'] = "APIAI"
        elif self.obj.ui.get_object("bing_radio").get_active():
            self.config['Main']['recogniser'] = "Bing"

        if self.obj.ui.get_object("dynamic_check_button").get_active():
            self.config['Main']['dynamic_noise_suppression'] = 'True'
        else:
            self.config['Main']['dynamic_noise_suppression'] = 'False'

        self.config['Google']['api_key'] = self.obj.ui.get_object("google_key_entry").get_text()
        self.config['Bing']['api_key'] = self.obj.ui.get_object("bing_key_entry").get_text()
        self.config['WITAI']['api_key'] = self.obj.ui.get_object("witai_key_entry").get_text()
        self.config['IBM']['username'] = self.obj.ui.get_object("ibm_username_entry").get_text()
        self.config['IBM']['password'] = self.obj.ui.get_object("ibm_password_entry").get_text()
        self.config['APIAI']['api_key'] = self.obj.ui.get_object("apiai_key_entry").get_text()
        super().save_settings(obj)


class SpeechConfigurableDialog(GObject.GObject):
    __gsignals__ = {
        'settings_changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, window):
        GObject.GObject.__init__(self)

        self.ui = Gtk.Builder()
        self.ui.add_from_file(SPEECH_SETTINGS_UI_PATH)
        self.dialog = self.ui.get_object("configure_dialog")
        self.dialog.set_transient_for(window)
        self.dialog.show_all()

        self.settings_handler = SpeechSettingsHandler(self)
        # simply update gui after each save
        self.settings_handler.connect('settings_loaded', self.on_settings_loaded)
        self.settings_handler.load_settings()

        self._connect_everything()

    def on_settings_loaded(self, settings_handler, config):
        self._update(config)

    def _update(self, config):
        self._choose_labelled_input_boxes(config)
        self._get_saved_into_text_boxes(config)
        self._populate_buttons(config)

    def _connect_everything(self):
        self.ui.get_object("sphinx_radio").connect("toggled", self._radio_callback)
        self.ui.get_object("bing_radio").connect("toggled", self._radio_callback)
        self.ui.get_object("google_radio").connect("toggled", self._radio_callback)
        self.ui.get_object("witai_radio").connect("toggled", self._radio_callback)
        self.ui.get_object("apiai_radio").connect("toggled", self._radio_callback)
        self.ui.get_object("ibm_radio").connect("toggled", self._radio_callback)

        self.ui.get_object("dynamic_check_button").connect("toggled", self._dynamic_check_callback)
        self.ui.get_object("default_button").connect("clicked", self._set_default_config)
        self.ui.get_object("close_button").connect("clicked", self.on_close_dialog)

    def _radio_callback(self, radio):
        self.emit('settings_changed')
        self._update(self.settings_handler.config)

    def _dynamic_check_callback(self, check):
        self.emit('settings_changed')

    def _set_default_config(self, button):
        default_config = self.settings_handler.default_settings()
        self._update(default_config)

    def on_close_dialog(self, button):
        self.emit('settings_changed')
        self.dialog.destroy()

    def _get_saved_into_text_boxes(self, config):
        _settings = config
        self.ui.get_object("google_key_entry").set_text(_settings['Google']['api_key'])
        self.ui.get_object("witai_key_entry").set_text(_settings['WITAI']['api_key'])
        self.ui.get_object("bing_key_entry").set_text(_settings['Bing']['api_key'])
        self.ui.get_object("ibm_username_entry").set_text(_settings['IBM']['username'])
        self.ui.get_object("ibm_password_entry").set_text(_settings['IBM']['password'])
        self.ui.get_object("apiai_key_entry").set_text(_settings['APIAI']['api_key'])

    def _populate_buttons(self, config):
        _settings = config

        if _settings['Main']['recogniser'] == "Sphinx":
            self.ui.get_object("sphinx_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "Google":
            self.ui.get_object("google_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "WITAI":
            self.ui.get_object("witai_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "IBM":
            self.ui.get_object("ibm_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "APIAI":
            self.ui.get_object("apiai_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "Bing":
            self.ui.get_object("bing_radio").set_active(True)

        if _settings['Main']['dynamic_noise_suppression'] == 'True':
            self.ui.get_object("dynamic_check_button").set_active(True)
        else:
            self.ui.get_object("dynamic_check_button").set_active(False)

    def _choose_labelled_input_boxes(self, config):
        # disable everything
        for child in self.ui.get_object("input_box"):
            child.set_sensitive(False)

        data = config['Main']['recogniser']
        if data == 'Google':
            self.ui.get_object("google_key_entry").set_sensitive(True)
            self.ui.get_object("google_key_label").set_sensitive(True)
        elif data == 'WITAI':
            self.ui.get_object("witai_key_entry").set_sensitive(True)
            self.ui.get_object("witai_key_label").set_sensitive(True)
        elif data == "Bing":
            self.ui.get_object("bing_key_entry").set_sensitive(True)
            self.ui.get_object("bing_key_label").set_sensitive(True)
        elif data == 'APIAI':
            self.ui.get_object("apiai_key_entry").set_sensitive(True)
            self.ui.get_object("apiai_key_label").set_sensitive(True)
        elif data == 'IBM':
            self.ui.get_object("ibm_username_entry").set_sensitive(True)
            self.ui.get_object("ibm_username_label").set_sensitive(True)
            self.ui.get_object("ibm_password_entry").set_sensitive(True)
            self.ui.get_object("ibm_password_label").set_sensitive(True)
