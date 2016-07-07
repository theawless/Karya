# Need not be a class right now, but later it might be needed
# currently uses xdotool, may change to PyAutoGui
import subprocess


class Writer:
    @staticmethod
    def inserttext(text, words=False):
        # a really odd way to capitalize the first letter would be to
        # select, copy last character, know if it is a space, then capitalize this
        subprocess.call(["xdotool", "type", text])
        pass

    @staticmethod
    def cut_clipboard():
        subprocess.call(["xdotool", "key", "ctrl+x"])
        pass

    @staticmethod
    def copy_clipboard():
        subprocess.call(["xdotool", "key", "ctrl+c"])
        pass

    @staticmethod
    def paste_clipboard():
        subprocess.call(["xdotool", "key", "ctrl+v"])

    @staticmethod
    def delete_selection():
        subprocess.call(["xdotool", "key", "BackSpace"])

    @staticmethod
    def select_all():
        subprocess.call(["xdotool", "key", "ctrl+a"])

    @staticmethod
    def delete_line():
        pass

    @staticmethod
    def delete_sentence():
        pass

    @staticmethod
    def undo():
        subprocess.call(["xdotool", "key", "ctrl+z"])

    @staticmethod
    def redo():
        subprocess.call(["xdotool", "key", "ctrl+shift+z"])

    @staticmethod
    def clear_document():
        subprocess.call(["xdotool", "key", "ctrl+a BackSpace"])
