# currently uses xdotool, may change to PyAutoGui
import subprocess


def inserttext(text, words=False):
    # a really odd way to capitalize the first letter would be to
    # select, copy last character, know if it is a space, then capitalize this
    subprocess.call(["xdotool", "type", text])
    pass


def cut_clipboard():
    subprocess.call(["xdotool", "key", "ctrl+x"])
    pass


def copy_clipboard():
    subprocess.call(["xdotool", "key", "ctrl+c"])
    pass


def paste_clipboard():
    subprocess.call(["xdotool", "key", "ctrl+v"])


def delete_selection():
    subprocess.call(["xdotool", "key", "BackSpace"])


def select_all():
    subprocess.call(["xdotool", "key", "ctrl+a"])


def delete_line():
    pass


def delete_sentence():
    pass


def undo():
    subprocess.call(["xdotool", "key", "ctrl+z"])


def redo():
    subprocess.call(["xdotool", "key", "ctrl+shift+z"])


def clear_document():
    subprocess.call(["xdotool", "key", "ctrl+a BackSpace"])
