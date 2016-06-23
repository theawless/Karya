import os
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Pango

SEARCH_LOCATION = os.path.expanduser('~')


class LocalSearch(GObject.GObject):
    __gsignals__ = {
        'result-found': (GObject.SIGNAL_RUN_FIRST, None, (str, str,))
    }

    def local_search(self, search_keywords):
        for root, dirs, files in os.walk(SEARCH_LOCATION):
            for file in files:
                if search_keywords in file:
                    # Getting full path of the file
                    path = os.path.join(root, file)
                    self.emit('result-found', path, file)

    def open_file(self, path):
        subprocess.call(("xdg-open", path))

    def append_to_list(self, list_box, item):
        (name, path) = item
        label = Gtk.Label(name)
        label.set_single_line_mode(True)
        label.set_line_wrap_mode(Pango.WrapMode.CHAR)
        button = Gtk.Button(label="Open")
        button.connect("clicked", self.open_file, path)
        hbox = Gtk.HBox(homogeneous=False)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(button, True, False, 0)
        row = Gtk.ListBoxRow()
        row.add(hbox)
        row.show_all()
        list_box.prepend(row)
