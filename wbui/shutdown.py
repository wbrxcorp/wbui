import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib

shutdown_page = None
shutdown_flag = None

class ShutdownPage(Gtk.Box):
    def __init__(self, main_window, mode=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.main_window = main_window
        self.mode = mode

        if mode != "INSTALLER":
            exit_button = Gtk.Button.new_with_mnemonic("タイトルに戻る(_X)" if mode == "LOGIN" else "終了(_X)")
            exit_button.connect("clicked", self.on_exit)
            self.append(exit_button)

        if mode is not None:
            shutdown_button = Gtk.Button.new_with_mnemonic("シャットダウン(_S)")
            shutdown_button.connect("clicked", self.on_shutdown)
            self.append(shutdown_button)
            reboot_button = Gtk.Button.new_with_mnemonic("再起動(_R)")
            reboot_button.connect("clicked", self.on_reboot)
            self.append(reboot_button)
    
    def on_exit(self, button):
        dlg = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK_CANCEL,modal=True,title="確認",transient_for=self.main_window)
        dlg.set_markup("タイトル画面へ戻ります。よろしいですか？" if self.mode == "LOGIN" else "終了してもよろしいですか？")
        dlg.connect('response', self.on_exit_response)
        dlg.show()
    
    def on_exit_response(self, dlg, response):
        dlg.destroy()
        if response == Gtk.ResponseType.OK: self.main_window.destroy()

    def on_shutdown(self, button):
        dlg = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK_CANCEL,modal=True,title="確認",transient_for=self.main_window)
        dlg.set_markup("システムをシャットダウンします。よろしいですか？")
        dlg.connect('response', self.on_shutdown_response)
        dlg.show()

    def on_shutdown_response(self, dlg, response):
        dlg.destroy()
        global shutdown_flag
        if response == Gtk.ResponseType.OK:
            shutdown_flag = "SHUTDOWN"
            self.main_window.destroy()

    def on_reboot(self, button):
        dlg = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK_CANCEL,modal=True,title="確認",transient_for=self.main_window)
        dlg.set_markup("システムを再起動します。よろしいですか？")
        dlg.connect('response', self.on_reboot_response)
        dlg.show()

    def on_reboot_response(self, dlg, response):
        dlg.destroy()
        global shutdown_flag
        if response == Gtk.ResponseType.OK:
            shutdown_flag = "REBOOT"
            self.main_window.destroy()

def get_instance():
    global shutdown_page, shutdown_flag
    if shutdown_page is not None: return shutdown_page
    #else
    shutdown_page = ShutdownPage()
    shutdown_flag = None
    return shutdown_page
