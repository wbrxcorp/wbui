import sys,getpass
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gtk, Gdk, GLib,GdkPixbuf, GObject
import pam,cairo

import wbui.theme

class PasswordDialog(Gtk.MessageDialog):
    def __init__(self, parent):
        self.parent = parent
        Gtk.MessageDialog.__init__(self, buttons=Gtk.ButtonsType.OK_CANCEL,modal=True,title="パスワード",transient_for=parent)
        self.invalid_password = Gtk.Label()
        self.invalid_password.set_markup("<span foreground=\"#ff0000\">パスワードが正しくありません</span>")
        self.invalid_password.set_visible(False)
        self.get_content_area().append(self.invalid_password)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        self.password_entry.set_visibility(False)
        self.password_entry.connect("activate", self.on_enter_key)
        self.get_content_area().append(self.password_entry)
        self.connect("response", self.on_response)
        self.present()
    def on_response(self, dlg, response):
        if response == Gtk.ResponseType.OK:
            self.on_enter_key(self.password_entry)
        else:
            self.emit("done", False)
            dlg.destroy()
    def on_enter_key(self, entry):
        if pam.authenticate(getpass.getuser(), entry.get_text(), service="wbui"):
            self.emit("done", True)
            self.destroy()
        else:
            self.invalid_password.set_visible(True)
            entry.set_text("")

GObject.signal_new("done", PasswordDialog, 0, None, (GObject.TYPE_BOOLEAN,))

def create_offscreen_buffer(width, height):
    surface = cairo.ImageSurface(cairo.Format.ARGB32, 1024, 768)
    return (cairo.Context(surface), surface)

def create_gtk_picture_from_surface(surface):
    return Gtk.Picture.new_for_pixbuf(Gdk.pixbuf_get_from_surface(surface, 0, 0, surface.get_width(), surface.get_height()))

class TitleWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application = app)
        context, surface = create_offscreen_buffer(1024, 768)

        background = wbui.theme.load_resource("title_background.png").scale_simple(surface.get_width(), surface.get_height(), GdkPixbuf.InterpType.BILINEAR)
        Gdk.cairo_set_source_pixbuf(context, background, 0, 0)
        context.paint()
        title = wbui.theme.load_resource("title.png")
        Gdk.cairo_set_source_pixbuf(context, title, (surface.get_width() - title.get_width()) / 2 , (surface.get_height() - title.get_height()) / 4)
        context.paint()
        context.set_source_rgba(0, 0, 0, 1)
        context.set_font_size(surface.get_height() / 22)
        copyright = "Copyright © 2009-2023 Walbrix Corporation"
        copyright_extents = context.text_extents(copyright)
        context.move_to((surface.get_width() - copyright_extents.width) / 2,  surface.get_height() - copyright_extents.height)
        context.show_text(copyright)
        image = create_gtk_picture_from_surface(surface)
        self.set_child(image)   # TODO: show hostname
        self.present()

        GLib.timeout_add(3, self.on_timeout)

    def on_timeout(self):
        dlg = Gtk.MessageDialog(buttons=Gtk.ButtonsType.OK,modal=True,title="ようこそ",transient_for=self)
        dlg.connect('response', self.on_enter_key)
        dlg.get_widget_for_response(Gtk.ResponseType.OK).set_label("Enterキーで続行")
        dlg.show()
        return False

    def on_enter_key(self, dlg, response):
        dlg.destroy()
        if response == Gtk.ResponseType.OK and pam.authenticate(getpass.getuser(), "", service="wbui"):
            self.destroy()
            return
        elif response != Gtk.ResponseType.OK:
            sys.exit(1)
        #else
        password_dlg = PasswordDialog(self)
        password_dlg.connect("done", self.on_password_done)
        password_dlg.show()
    
    def on_password_done(self, dlg, success):
        if success:
            self.destroy()
        else:
            self.on_timeout()

