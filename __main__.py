import os,sys,subprocess

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import wbui, wbui.login, wbui.shutdown

if __name__ == "__main__":
    login = False
    if len(sys.argv) > 1:
        subcommand = sys.argv[1]
        if subcommand == "login":
            app = Gtk.Application()
            app.connect("activate", lambda x: wbui.login.TitleWindow(app))
            app.run()
            login = True
        elif subcommand == "installer":
            os.execlp("weston-terminal", "weston-terminal", "--shell=/usr/bin/installer")

    #os.execlp("weston-terminal", "weston-terminal")
    app = Gtk.Application()
    app.connect("activate", lambda x: wbui.MainWindow(app, login))
    app.run()
    if wbui.shutdown.shutdown_flag == "SHUTDOWN":
        subprocess.call("poweroff")
    if wbui.shutdown.shutdown_flag == "REBOOT":
        subprocess.call("reboot")
