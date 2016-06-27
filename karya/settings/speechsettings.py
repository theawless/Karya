import configparser
import copy

from gi.repository import Gtk, GObject

from utilities.variables import CONFIG_INI_PATH, CONFIG_UI_PATH


# LEGACY code - very old
class SpeechSettingsHandler(GObject.GObject):
    # a static variable in all instances
    speech_settings = dict()
    __gsignals__ = {
        'changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.load_settings()

    @staticmethod
    def default_settings():
        config = configparser.ConfigParser()
        config['Main'] = {'recogniser': 'WITAI', 'dynamic_noise_suppression': 'False'}
        config['Sphinx'] = {'version': 'pocketsphinx'}
        config['Google'] = {'api_key': ''}
        config['WITAI'] = {'api_key': ''}
        config['APIAI'] = {'api_key': ''}
        config['Bing'] = {'api_key': ''}
        config['IBM'] = {'username': '', 'password': ''}
        return config

    @staticmethod
    def config_to_dict(config: configparser.ConfigParser):
        settings_dictionary = {}
        for sect in config.sections():
            settings_dictionary[sect] = {}
            for opt in config.options(sect):
                settings_dictionary[sect][opt] = config.get(sect, opt)
        return settings_dictionary

    def load_settings(self):
        config = self.default_settings()
        config.read(CONFIG_INI_PATH)
        self.__class__.speech_settings = self.config_to_dict(config)

    def save_settings(self, settings: dict):
        config = self.default_settings()
        config['Main'] = {'recogniser': settings['Main']['recogniser'],
                          'dynamic_noise_suppression': settings['Main']['dynamic_noise_suppression']}
        config['Google'] = {'api_key': settings['Google']['api_key']}
        config['WITAI'] = {'api_key': settings['WITAI']['api_key']}
        config['APIAI'] = {'api_key': settings['APIAI']['api_key']}
        config['Bing'] = {'api_key': settings['Bing']['api_key']}
        config['IBM'] = {'username': settings['IBM']['username'], 'password': settings['IBM']['password']}
        # write new values to the configuration file
        with open(CONFIG_INI_PATH, 'w+') as configfile:
            config.write(configfile)
        self.__class__.speech_settings = settings
        self.emit('changed')


class ConfigurableDialog:
    def __init__(self, window):
        self.settings_handler = SpeechSettingsHandler()
        self.settings = copy.deepcopy(self.settings_handler.speech_settings)
        self.ui = Gtk.Builder()
        self.ui.add_from_file(CONFIG_UI_PATH)
        self.dialog = self.ui.get_object("configure_dialog")
        self.setup_dialog()
        self.dialog.set_transient_for(window)
        self.dialog.show_all()

    def setup_dialog(self):
        self._get_saved_into_text_boxes()
        self._choose_labelled_input_boxes()
        self._connect_everything()
        self._populate_buttons()

    def on_close_dialog(self, button):
        self.dialog.destroy()

    def _get_saved_into_text_boxes(self):
        _settings = self.settings
        self.ui.get_object("google_key_entry").set_text(_settings['Google']['api_key'])
        self.ui.get_object("witai_key_entry").set_text(_settings['WITAI']['api_key'])
        self.ui.get_object("bing_key_entry").set_text(_settings['Bing']['api_key'])
        self.ui.get_object("ibm_username_entry").set_text(_settings['IBM']['username'])
        self.ui.get_object("ibm_password_entry").set_text(_settings['IBM']['password'])
        self.ui.get_object("apiai_key_entry").set_text(_settings['APIAI']['api_key'])

    def _connect_everything(self):
        self.ui.get_object("sphinx_radio").connect("toggled", self._radio_callback, "Sphinx")
        self.ui.get_object("bing_radio").connect("toggled", self._radio_callback, "Bing")
        self.ui.get_object("google_radio").connect("toggled", self._radio_callback, "Google")
        self.ui.get_object("witai_radio").connect("toggled", self._radio_callback, "WITAI")
        self.ui.get_object("apiai_radio").connect("toggled", self._radio_callback, "APIAI")
        self.ui.get_object("ibm_radio").connect("toggled", self._radio_callback, "IBM")
        self.ui.get_object("save_button").connect("clicked", self._confirm_config)
        self.ui.get_object("default_button").connect("clicked", self._set_default_config)
        self.ui.get_object("dynamic_check_button").connect("toggled", self._dynamic_check_callback)
        self.ui.get_object("save_button").connect("clicked", self._confirm_config)
        self.ui.get_object("default_button").connect("clicked", self._set_default_config)
        self.ui.get_object("close_button").connect("clicked", self.on_close_dialog)

    def _populate_buttons(self):
        _settings = self.settings

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

    def _choose_labelled_input_boxes(self):
        # Disable everything
        for child in self.ui.get_object("input_box"):
            child.set_sensitive(False)

        data = self.settings['Main']['recogniser']
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

    def _radio_callback(self, radio, data):
        if radio.get_active():
            # All radio_callback are called simultaneously, checking which one went active
            self.settings['Main']['recogniser'] = data
            self._choose_labelled_input_boxes()

    def _dynamic_check_callback(self, check):
        self.settings['Main']['dynamic_noise_suppression'] = str(check.get_active())

    def _set_default_config(self, button):
        # load default settings and save them by calling mainsettings class
        self.settings = self.settings_handler.config_to_dict(self.settings_handler.default_settings())
        self.settings_handler.save_settings(self.settings)
        self._get_saved_into_text_boxes()
        self._populate_buttons()

    def _confirm_config(self, button):
        # save input values to temporary settings
        self.settings['Google']['api_key'] = self.ui.get_object("google_key_entry").get_text()
        self.settings['Bing']['api_key'] = self.ui.get_object("bing_key_entry").get_text()
        self.settings['WITAI']['api_key'] = self.ui.get_object("witai_key_entry").get_text()
        self.settings['IBM']['username'] = self.ui.get_object("ibm_username_entry").get_text()
        self.settings['IBM']['password'] = self.ui.get_object("ibm_password_entry").get_text()
        self.settings['APIAI']['api_key'] = self.ui.get_object("apiai_key_entry").get_text()
        # save to main settings
        self.settings_handler.save_settings(self.settings)
