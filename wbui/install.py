import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk

import wbui,wbui.process

class Header(Gtk.DrawingArea):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.background = wbui.theme.load_resource("header.png")
        self.logo = wbui.theme.load_resource("header_logo.png")
        self.set_content_width(self.background.get_width())
        self.set_content_height(self.background.get_height())
        self.set_draw_func(self.on_draw)
    def on_draw(self, drawing_area, context, width, height):
        Gdk.cairo_set_source_pixbuf(context, self.background, 0, 0)
        context.paint()
        Gdk.cairo_set_source_pixbuf(context, self.logo, 0, 0)
        context.paint()

class InstallerPage(Gtk.Box):
    def __init__(self, parent):
        self.parent = parent
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, vexpand=True)
        self.append(Gtk.Label(
            label="インストールを開始するには、インストール先のディスクを選択して\n「インストール開始」ボタンを押してください。",
            margin_top=8, margin_start=8, margin_end=8
        ))
        self.liststore = Gtk.ListStore(str,str,str,str)
        self.treeview = Gtk.TreeView(model=self.liststore, margin_top=8,margin_start=8,margin_end=8)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("デバイス名", renderer, text=0)
        self.treeview.append_column(column)
        column = Gtk.TreeViewColumn("機種", renderer, text=1)
        self.treeview.append_column(column)
        column = Gtk.TreeViewColumn("接続", renderer, text=2)
        self.treeview.append_column(column)
        column = Gtk.TreeViewColumn("容量", renderer, text=3)
        self.treeview.append_column(column)
        self.treeview.get_selection().connect("changed", self.on_tree_selection_changed)
        self.append(self.treeview)

        self.start_button = Gtk.Button.new_with_mnemonic("インストール開始(_I)")
        self.start_button.set_margin_top(8)
        self.start_button.set_margin_start(8)
        self.start_button.set_margin_end(8)
        self.start_button.connect("clicked", self.start_install)
        self.start_button.set_sensitive(False)
        self.append(self.start_button)
        wbui.process.WbSimpleInvoke({"execute":"get-usable-disks-for-install"}, self.get_usable_disks_done)

    def get_usable_disks_done(self, status, result, stderr):
        if status != 0 or "return" not in result:
            wbui.footer.get_instance().set_message("ディスク一覧の取得に失敗しました")
            return
        #else
        #self.start_button.set_sensitive(True)
        self.liststore.clear()
        for disk in result["return"]:
            self.liststore.append([
                disk["name"], 
                disk["model"] if "model" in disk else "-",
                disk["tran"] if "tran" in disk else "-",
                "%dGB" % (disk["size"] / 1024.0 / 1024 / 1024)])
    
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        self.start_button.set_sensitive(treeiter is not None)

    def start_install(self, btn):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter is None: return
        #else
        disk = model[treeiter][0]
        dlg = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK_CANCEL,modal=True,title="確認",transient_for=self.parent)
        dlg.set_markup("<b>選択された記録媒体 %s の内容は完全に消去されます</b>。\nインストールを続行してもよろしいですか？" % disk)
        def on_response(dlg,response):
            dlg.destroy()
            if response == Gtk.ResponseType.OK:
                wbui.process.WbStreamInvoke(self.parent, "インストール中...", 
                    {"execute":"install","arguments":disk}, self.done_installation)
        dlg.connect('response', on_response)
        dlg.show()

    def done_installation(self, status, stderr):
        if status == 0: 
            dlg = Gtk.MessageDialog(buttons = Gtk.ButtonsType.OK, modal = True, 
                text = "インストールが完了しました。\nシステムを再起動します。", transient_for=self.parent)
            def on_response(dlg, response):
                dlg.destroy()
                self.parent.destroy()
            dlg.connect('response', on_response)
            dlg.show()
        elif status == 15:
            dlg = Gtk.MessageDialog(buttons = Gtk.ButtonsType.OK, modal = True, 
                text = "インストールを中断しました", transient_for=self.parent)
            dlg.connect('response', lambda dlg,res : dlg.destroy())
            dlg.show()
        else:
            dlg = Gtk.MessageDialog(buttons = Gtk.ButtonsType.OK, modal = True, 
                text = "インストールに失敗しました。 %s" % (stderr), transient_for=self.parent)
            dlg.connect('response', lambda dlg,res : dlg.destroy())
            dlg.show()

class InstallerWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application = app)
        self.set_default_size(wbui.WINDOW_WIDTH, wbui.WINDOW_HEIGHT)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox.append(Header())

        vbox.append(InstallerPage(self))
        
        footer = wbui.footer.get_instance()
        vbox.append(footer)
        footer.set_message("Walbrixインストーラーへようこそ")

        self.set_child(vbox)
        self.present()
