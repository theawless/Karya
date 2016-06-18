import sys

import gi

from shell.application import Application

gi.require_version('Gtk', '3.0')

app = Application()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
