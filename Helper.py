import threading
import gtk.gdk

'''
Calls a after a specific time in a different thread.
'''
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

'''
Gives me the pixel at a specific position super fast.
'''
def pixel_at(x, y):
    gtk.gdk
    rw = gtk.gdk.get_default_root_window()
    pixbuff = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
    pixbuff = pixbuff.get_from_drawable(rw, rw.get_colormap(), x, y, 0, 0, 1, 1)
    return tuple(pixbuff.pixel_array[0, 0])

