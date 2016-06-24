import gi

gi.require_version('PeasGtk', '1.0')
gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Peas, PeasGtk

from utilities.variables import DEFAULT_PLUGIN_PATH, LOADED_PLUGIN_INI_PATH


class PluginManager:
    def __init__(self, activator):
        self.activator = activator

        self.plugin_engine = Peas.Engine()
        self.plugin_engine.add_search_path(DEFAULT_PLUGIN_PATH, DEFAULT_PLUGIN_PATH)
        self.plugin_engine.enable_loader('python3')

        self.extension_set = Peas.ExtensionSet.new(self.plugin_engine, Peas.Activatable, [])
        self.extension_set.connect("extension-added", self.on_extension_added)
        self.extension_set.connect("extension-removed", self.on_extension_removed)

        self.load_saved_plugins()
        # After we load plugin we connect to these signals, now we can edit the saved file.
        self.plugin_engine.connect_after("load-plugin", self.update_saved_loaded_plugins)
        self.plugin_engine.connect_after("unload-plugin", self.update_saved_loaded_plugins)

    def add_gui(self, window):
        dialog = Gtk.Dialog()
        dialog.set_transient_for(window)
        dialog.set_modal(True)
        plugin_ui = PeasGtk.PluginManager(self.plugin_engine)
        dialog.get_content_area().pack_start(plugin_ui, True, True, 0)
        plugin_ui.set_homogeneous(False)
        dialog.show_all()

    def on_extension_added(self, set, info, activatable):
        activatable.get_activator(self.activator)
        activatable.activate()

    def on_extension_removed(self, set, info, activatable):
        activatable.deactivate()

    def update_saved_loaded_plugins(self, engine=None, plugin=None):
        with open(LOADED_PLUGIN_INI_PATH, 'w+') as file:
            for plugin in self.plugin_engine.get_loaded_plugins():
                file.write(plugin + '\n')

    def load_saved_plugins(self):
        try:
            with open(LOADED_PLUGIN_INI_PATH, 'r') as file:
                load_list = [line.rstrip() for line in file]
                self.plugin_engine.set_loaded_plugins(load_list)
        except FileNotFoundError:
            self.update_saved_loaded_plugins()
