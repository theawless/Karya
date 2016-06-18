import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango


class LocalSearch:
    def __init__(self):
        pass

    def local_search(self, search_keywords, location):
        search_result_paths = ["" for x in range(2000)]
        search_result_names = ["" for x in range(2000)]
        l = []
        i = 0
        for root, dirs, files in os.walk('~'):
            for file in files:
                if search_keywords in file:
                    # Getting full path of the file
                    path = os.path.join(root, file)
                    search_result_names[i] = file
                    tup = str(path), str(file)
                    l.append(tup)
                    print(search_result_names[i])
                    search_result_paths[i] = path
                    i += 1
        return l

    def open_file_shown_in_search_result(self, button, file_path):
        print("Path is " + file_path)
        open_file(file_path)

    def show_local_search_result(self, builder, input_text):
        search_res_listbox = builder.get_object("list_box")
        clean(search_res_listbox)
        tup_list = local_search(input_text)
        for (path, name) in tup_list:
            label = Gtk.Label(name)
            label.set_single_line_mode(True)
            label.set_line_wrap_mode(Pango.WrapMode.CHAR)
            button = Gtk.Button.new_with_label("Open")
            button.connect("clicked", open_file_shown_in_search_result, path)
            row = Gtk.ListBoxRow()
            hbox = Gtk.HBox()
            hbox.set_homogeneous(True)
            hbox.pack_start(label, True, True, 0)
            hbox.pack_start(button, True, False, 0)
            row.add(hbox)
            search_res_listbox.prepend(row)
        search_res_listbox.show_all()
