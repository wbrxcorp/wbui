import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,GLib

from wbui import theme 

footer = None

class Footer(Gtk.DrawingArea):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.background = theme.load_resource("footer.png")
        self.set_content_width(self.background.get_width())
        self.set_content_height(self.background.get_height())
        self.set_draw_func(self.on_draw)
    def set_message(self, message):
        self.message = message
        self.queue_draw()
    def on_draw(self, drawing_area, context, width, height):
        Gdk.cairo_set_source_pixbuf(context, self.background, 0, 0)
        context.paint()
        context.set_source_rgba(1, 1, 1, 1)
        context.set_font_size(height / 2)
        text_extents = context.text_extents(self.message)
        margin = (height - text_extents.height) / 2
        context.move_to(margin,  height - margin)
        context.show_text(self.message)

def get_instance():
    global footer
    if footer is not None: return footer
    #else
    footer = Footer()
    return footer
