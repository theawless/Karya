from abc import abstractmethod
from enum import Enum


class WindowModes(Enum):
    large = True
    small = False


# An interface for all elements that change with window modes
class WindowModeSubscribers:
    def __init__(self, app):
        if app is not None:
            app.connect('mode_changed', self.on_window_change)

    def on_window_change(self, app, mode):
        if mode == WindowModes.small:
            self.on_window_change_small()
        elif mode == WindowModes.large:
            self.on_window_change_large()

    # these will be called appropriately

    @abstractmethod
    def on_window_change_small(self):
        pass

    @abstractmethod
    def on_window_change_large(self):
        pass
