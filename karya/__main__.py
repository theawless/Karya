import logging
import os
import sys

import gi

from shell.application import Application
from utilities.variables import LOG_DIR_PATH

gi.require_version('Gtk', '3.0')


def main():
    _setup_logger()
    app = Application()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


def _setup_logger():
    if not os.path.exists(LOG_DIR_PATH):
        os.makedirs(LOG_DIR_PATH)

    logger = logging.getLogger()
    formatter = logging.Formatter('%(threadName)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    log_file = LOG_DIR_PATH + 'log.txt'
    fh = logging.FileHandler(log_file, 'w')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# to prevent imports
if __name__ == "__main__":
    main()
