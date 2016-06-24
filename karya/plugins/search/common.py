import gi

gi.require_version('Gtk', '3.0')
from .LocalSearch import LocalSearch
from .OnlineSearch import OnlineSearch
import threading

class SearchCommon:
    def __init__(self, ui):
        self.local_searcher = LocalSearch()
        self.online_searcher = OnlineSearch()
        self.ui = ui
        self.local_list = self.ui.get_object('LocalListBox')
        self.local_list.show()
        self.online_list = self.ui.get_object('OnlineListBox')
        self.search_entry = self.ui.get_object('SearchEntry')
        self.search_entry.connect('search_changed', self.search_changed)
        self.local_searcher.connect('result-found', self.result_found)
        self.search_thread=threading.main_thread()

    def result_found(self, local_searcher, path, file):
        print('result_found' + str(file) + str(path))
        self.local_searcher.append_to_list(self.local_list, (path, file))

    def search_changed(self, search_entry):
        self.local_searcher.local_search(search_entry.get_text())
        print('search_changed_signal')
