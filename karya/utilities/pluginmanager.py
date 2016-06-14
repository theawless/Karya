import gi

gi.require_version('PeasGtk', '1.0')
gi.require_version('Peas', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Peas, PeasGtk

from utilities.variables import DEFAULT_PLUGIN_PATH


class PluginManager:
    def __init__(self):
        self.plugin_engine = Peas.Engine()
        self.plugin_engine.add_search_path(DEFAULT_PLUGIN_PATH, DEFAULT_PLUGIN_PATH)
        self.plugin_engine.enable_loader('python3')

        self.plugin_ui = PeasGtk.PluginManager(self.plugin_engine)

        self.extension_set = Peas.ExtensionSet.new(self.plugin_engine, Peas.Activatable, [])
        self.extension_set.connect("extension-added", self.on_extension_added)
        self.extension_set.connect("extension-removed", self.on_extension_removed)

    def add_gui(self, window):
        dialog = Gtk.Dialog()
        dialog.set_transient_for(window)
        box = dialog.get_content_area()
        box.add(self.plugin_ui)
        dialog.show_all()

    def on_extension_added(self, set, info, activatable):
        activatable.get_data()
        activatable.activate()

    def on_extension_removed(self, set, info, activatable):
        activatable.deactivate()
