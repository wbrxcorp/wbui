import os,sys

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from wbui import login

if __name__ == "__main__":
    if len(sys.argv) > 1:
        subcommand = sys.argv[1]
        if subcommand == "login":
            app = Gtk.Application(application_id="com.walbrix.WBUILogin")
            app.connect("activate", lambda x: login.TitleWindow(app))
            app.run()
        elif subcommand == "installer":
            os.execlp("weston-terminal", "weston-terminal", "--shell=/usr/bin/installer")

    os.execlp("weston-terminal", "weston-terminal")
