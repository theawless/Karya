import logging

from settings.configurationhandler import ConfigurationHandler, ListConfigParser
from shell.windowelements import WindowModes
from utilities.variables import LOADED_PLUGIN_INI_PATH, WINDOW_STATE_INI_PATH

logger = logging.getLogger(__name__)


class WindowConfigurationHandler(ConfigurationHandler):
    config = ListConfigParser()

    def __init__(self, app):
        super().__init__(self.config, WINDOW_STATE_INI_PATH)
        app.connect('settings_changed', self.save_settings)

    def save_settings(self, app):
        window = app.current_window
        name = window.mode.name
        self.config['Main'] = {'Window': name}
        position = window.get_position()
        size = window.get_size()
        self.config[name] = {'position_X': position[0], 'position_Y': position[1],
                             'size_X': size[0], 'size_Y': size[1]}
        super().save_settings()

    def default_settings(self):
        self.config['Main'] = {'Window': WindowModes.large.name}
        self.config[WindowModes.large.name] = {'position_X': 0, 'position_Y': 0, 'size_X': 800,
                                               'size_Y': 500}
        self.config[WindowModes.small.name] = {'position_X': 0, 'position_Y': 0, 'size_X': 1,
                                               'size_Y': 1}


class PluginConfigurationHandler(ConfigurationHandler):
    config = ListConfigParser()

    def __init__(self, plugin_manager, default_plugins):
        self.default_plugins = default_plugins
        super().__init__(self.config, LOADED_PLUGIN_INI_PATH)
        plugin_manager.connect('settings_changed', self.save_settings)

    def save_settings(self, obj):
        plugin_list = obj.plugin_engine.get_loaded_plugins()
        self.config.save_list('Main', 'loaded_plugins', plugin_list)
        super().save_settings()

    def default_settings(self):
        self.config['Main'] = {'loaded_plugins': ''}
        self.config.save_list('Main', 'loaded_plugins', self.default_plugins)
