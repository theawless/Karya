import gi

gi.require_version('PeasGtk', '1.0')
gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Peas, PeasGtk

from utilities.variables import DEFAULT_PLUGIN_PATH
from settings.mainsettings import PluginConfigurationHandler
from gi.repository import GObject

import logging

logger = logging.getLogger(__name__)


class PluginManager(GObject.GObject):
    __gsignals__ = {
        'settings_changed': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, activator):
        GObject.GObject.__init__(self)
        # an alternate to activatable
        self.activator = activator

        self.plugin_engine = Peas.Engine()
        self.plugin_engine.add_search_path(DEFAULT_PLUGIN_PATH, DEFAULT_PLUGIN_PATH)
        self.plugin_engine.enable_loader('python3')

        # getting weird GObject.Parameter errors, hence the different way of activatable - notice the empty list
        self.extension_set = Peas.ExtensionSet.new(self.plugin_engine, Peas.Activatable, [])

        self.extension_set.connect("extension-added", self.on_extension_added)
        self.extension_set.connect("extension-removed", self.on_extension_removed)

        self.settings_handler = PluginConfigurationHandler(self, [''])
        self.settings_handler.connect('settings_loaded', self.on_settings_loaded)
        self.settings_handler.load_settings()
        self.plugin_engine.connect_after("load-plugin", self.on_load_plugin)
        self.plugin_engine.connect_after("unload-plugin", self.on_unload_plugin)

    def on_settings_loaded(self, settings_handler, config):
        self.plugin_engine.set_loaded_plugins(config.get_list('Main', 'loaded_plugins'))

    def on_load_plugin(self, plugin_engine, plugin):
        self.emit('settings_changed')

    def on_unload_plugin(self, plugin_engine, plugin):
        self.emit('settings_changed')

    def add_gui(self, window):
        dialog = Gtk.Dialog()
        dialog.set_transient_for(window)
        dialog.set_modal(True)
        plugin_ui = PeasGtk.PluginManager(self.plugin_engine)
        dialog.get_content_area().pack_start(plugin_ui, True, True, 0)
        plugin_ui.set_homogeneous(False)
        dialog.show_all()

    def on_extension_added(self, set, info, activatable):
        # main difference from how normal libpeas plugin system works
        activatable.get_activator(self.activator)
        activatable.activate()

    def on_extension_removed(self, set, info, activatable):
        activatable.deactivate()
