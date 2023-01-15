import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,GLib

import gettext,getpass

import pam

#import pyte

import wbui.login

class TestWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application = app)
        self.present()
        GLib.timeout_add(1, self.on_timeout)
    def on_timeout(self):
        self.dlg = wbui.login.PasswordDialog(self)
        self.dlg.connect("done", self.on_done)
        self.dlg.show()
    def on_done(self, dlg, success):
        print("succeeded" if success else "cancelled")
        self.destroy()

if __name__ == "__main__":
    #print(gettext.find("wbui", "./locale",["ja"]))

    app = Gtk.Application(application_id="com.walbrix.WBUITest")
    app.connect("activate", lambda x: wbui.login.TitleWindow(app))
    app.run()
