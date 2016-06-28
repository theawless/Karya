# an alternative to activatable
# private variables and public functions which shall be provided to the plugins
import logging

logger = logging.getLogger(__name__)


class Activator:
    def __init__(self, app, window, home, speech_recogniser):
        self._app = app
        self._window = window
        self._home = home
        self._speech_recogniser = speech_recogniser

    def add_gui(self, name, title, stack_box, plugins_box=None):
        if name == '' or title == '' or stack_box is None:
            logger.debug('Trying to add empty stuff to home')
            return
        if self._home.stack.get_child_by_name(name) is not None:
            logger.debug('Adding child twice')
            return
        self._home.add_to_stack(name, title, stack_box)
        if plugins_box is None:
            logger.debug('Not adding menu')
            return
        self._window.add_plugin_menu_box(plugins_box)

    def get_home_stack(self):
        return self._home.stack
