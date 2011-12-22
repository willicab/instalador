import gtk

def exit(*args):
    raise SystemExit

def main():
    w = gtk.Window()
    w.connect("destroy", exit)
    f = gtk.Frame()
    b = gtk.Button("Hello World!")
    b.connect("clicked", exit)
    f.set_border_width(2)
    f.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535))
    f.add(b)
    w.add(f)
    w.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

