import subprocess

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib

import wbui.process,wbui.theme,wbui.header,wbui.footer,wbui.shutdown

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

class StatusPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label()
        label.set_markup("STATUS PAGE TBD")
        self.append(label)

class ConsolePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label()
        label.set_markup("コンソールから戻るには exit と入力してください。")
        self.append(label)
        open_button = Gtk.Button.new_with_mnemonic("Linuxコンソールを開く(_C)")
        open_button.connect("clicked", self.on_open)
        self.append(open_button)
    def on_open(self, button):
        subprocess.call("weston-terminal")

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app, login):
        Gtk.ApplicationWindow.__init__(self, application = app)
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox.append(wbui.header.get_instance())

        # setup main stack
        stack = Gtk.Stack()
        stack.add_titled(StatusPage(), "status", "状態")
        stack.add_titled(ConsolePage(), "console", "Linuxコンソール")
        stack.add_titled(wbui.shutdown.ShutdownPage(self, login), "shutdown", "終了と再起動" if login else "終了")

        sidebar = Gtk.StackSidebar()
        sidebar.set_stack(stack)

        sidebar_stack_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        sidebar_stack_box.append(sidebar)
        sidebar_stack_box.append(stack)
        sidebar_stack_box.set_vexpand(True)

        vbox.append(sidebar_stack_box)
        
        footer = wbui.footer.get_instance()
        vbox.append(footer)
        footer.set_message("Walbrixへようこそ")

        self.set_child(vbox)
        self.present()

    def on_click(self, btn):
        print("clicked!")
        dialog = wbui.process.ProcessExecutionDialog(self, ["files/wb"], lambda x, y, z: print(x, y, z))

