class Activator:
    def __init__(self, app, window, home, speech_recogniser):
        self._app = app
        self._window = window
        self._home = home
        self._speech_recogniser = speech_recogniser

    def add_to_home(self, name, title, box):
        if name == '' or title == '' or box is None:
            return
        self._home.add_to_stack(name, title, box)

    def add_to_plugins_menu(self, box):
        if box is None:
            return
        self._window.add_plugin_menu_box(box)
