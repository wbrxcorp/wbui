import subprocess

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class ConsolePage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label()
        label.set_markup("コンソールから戻るには exit と入力してください。")
        self.append(label)
        open_button = Gtk.Button.new_with_mnemonic("Linuxコンソールを開く(_C)")
        open_button.connect("clicked", lambda btn: subprocess.call("weston-terminal"))
        self.append(open_button)
