import configparser
import logging
from abc import abstractmethod

from gi.repository import GObject

logger = logging.getLogger(__name__)


class ListConfigParser(configparser.ConfigParser):
    def save_list(self, section, option, seq):
        string = ','.join(map(str, seq))
        self[section][option] = string

    def get_list(self, section, option):
        seq = self[section][option].split(',')
        return seq

    def config_to_dict(self):
        config = self
        settings_dictionary = {}
        for sect in config.sections():
            settings_dictionary[sect] = {}
            for opt in config.options(sect):
                settings_dictionary[sect][opt] = config.get(sect, opt)
        return settings_dictionary


# maybe we will replace it with an implementation of gsettings
class ConfigurationHandler(GObject.GObject):
    __gsignals__ = {
        'settings_loaded': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'settings_saved': (GObject.SIGNAL_RUN_FIRST, None, (object,))
    }

    # acting as multiple constructor
    def __init__(self, config, obj=None, ini_path=None):
        GObject.GObject.__init__(self)
        # config we receive here is derived class' class variable
        self.config = config
        self.ini_path = ini_path
        if obj is not None:
            self.obj = obj
            # must have settings_changed signal in obj
            self.obj.connect('settings_changed', self.save_settings)
        self.load_settings()

    # virtual methods

    def save_settings(self, obj):
        with open(self.ini_path, 'w+') as configfile:
            self.config.write(configfile)
        self.emit('settings_saved', self.config)

    def load_settings(self):
        self.default_settings()
        self.config.read(self.ini_path)
        self.emit('settings_loaded', self.config)

    @abstractmethod
    def default_settings(self):
        pass
