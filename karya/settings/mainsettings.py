import logging

from settings.configurationhandler import ConfigurationHandler
from shell.windowelements import WindowModes
from utilities.variables import WINDOW_STATE_INI_PATH, LOADED_PLUGIN_INI_PATH

logger = logging.getLogger(__name__)


class WindowConfigurationHandler(ConfigurationHandler):
    def __init__(self, window):
        super().__init__(window, WINDOW_STATE_INI_PATH)

    def save_settings(self, obj):
        # TO DO modify gravity for better placement
        self.config['Main'] = {'Window': self.obj.window_mode.name}
        size = self.obj.get_size()
        position = self.obj.get_position()
        self.config[self.obj.window_mode.name] = {'position_X': position[0], 'position_Y': position[1],
                                                  'size_X': size[0], 'size_Y': size[1]}
        super().save_settings(obj)

    def default_settings(self):
        self.config['Main'] = {'Window': WindowModes.large.name}
        self.config[WindowModes.large.name] = {'position_X': 0, 'position_Y': 0, 'size_X': 800,
                                               'size_Y': 500}
        self.config[WindowModes.small.name] = {'position_X': 0, 'position_Y': 0, 'size_X': 1,
                                               'size_Y': 1}


class PluginConfigurationHandler(ConfigurationHandler):
    def __init__(self, plugin_manager, default_plugins):
        self.default_plugins = default_plugins
        super().__init__(plugin_manager, LOADED_PLUGIN_INI_PATH)

    def save_settings(self, obj):
        plugin_list = self.obj.plugin_engine.get_loaded_plugins()
        self.config.save_list('Main', 'loaded_plugins', plugin_list)
        super().save_settings(obj)

    def default_settings(self):
        self.config['Main'] = {'loaded_plugins': ''}
        self.config.save_list('Main', 'loaded_plugins', self.default_plugins)
