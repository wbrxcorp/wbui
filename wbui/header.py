from datetime import datetime

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib

import wbui

header = None

class Header(Gtk.DrawingArea):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.background = wbui.theme.load_resource("header.png")
        self.logo = wbui.theme.load_resource("header_logo.png")
        self.set_content_width(self.background.get_width())
        self.set_content_height(self.background.get_height())
        self.set_draw_func(self.on_draw)
        GLib.timeout_add(1000, self.on_timeout)
    def on_draw(self, drawing_area, context, width, height):
        Gdk.cairo_set_source_pixbuf(context, self.background, 0, 0)
        context.paint()
        Gdk.cairo_set_source_pixbuf(context, self.logo, 0, 0)
        context.paint()
        context.set_source_rgba(1, 1, 1, 1)
        context.set_font_size(height / 2)
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M") if now.second % 2 == 0 else now.strftime("%Y-%m-%d %H %M")
        text_extents = context.text_extents(time)
        margin = (height - text_extents.height) / 2
        context.move_to(width - text_extents.width - margin,  height - margin)
        context.show_text(time)

    def on_timeout(self):
        self.queue_draw()
        return True

def get_instance():
    global header
    if header is not None: return header
    #else
    header = Header()
    return header
