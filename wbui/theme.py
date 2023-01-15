import pkgutil

import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf

def load_resource(resource_name):
    loader = GdkPixbuf.PixbufLoader()
    loader.write(pkgutil.get_data("wbui.default_theme", resource_name))
    loader.close()
    return loader.get_pixbuf()
