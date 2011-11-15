import gobject
import pygtk
pygtk.require('2.0')
import gtk
import multiprocessing
import threading
import time

gtk.gdk.threads_init()

class Listener(gobject.GObject):
    __gsignals__ = {
        'updated' : (gobject.SIGNAL_RUN_LAST,
                     gobject.TYPE_NONE,
                     (gobject.TYPE_FLOAT, gobject.TYPE_STRING)),
        'finished': (gobject.SIGNAL_RUN_LAST,
                     gobject.TYPE_NONE,
                     ())
    }

    def __init__(self, queue):
        gobject.GObject.__init__(self)
        self.queue = queue

    def go(self):
        print "Listener has started"
        while True:
            # Listen for results on the queue and process them accordingly                            
            data = self.queue.get()
            # Check if finished                                                                       
            if data[1]=="finished":
                print "Listener is finishing."
                self.emit("finished")
                return
            else:
                self.emit('updated', data[0], data[1])

gobject.type_register(Listener)

class Worker():
    def __init__(self, queue):
        self.queue = queue

    def go(self):
        print "The worker has started doing some work (counting from 0 to 9)"
        for i in range(10):
            proportion = (float(i+1))/10
            self.queue.put((proportion, "working..."))
            time.sleep(0.5)
        self.queue.put((1.0, "finished"))
        print "The worker has finished."


class Interface:
    def __init__(self):
        self.process = None
        self.progress = gtk.ProgressBar()
        button = gtk.Button("Go!")
        button.connect("clicked", self.go)
        vbox = gtk.VBox(spacing=5)
        vbox.pack_start(self.progress)
        vbox.pack_start(button)
        vbox.show_all()
        self.frame = vbox

    def main(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        window.add(self.frame)
        window.show()
        window.connect("destroy", self.destroy)

        gtk.main()

    def destroy(self, widget, data=None):
        gtk.main_quit()


    def callbackDisplay(self, obj, fraction, text, data=None):
        self.progress.set_fraction(fraction)
        self.progress.set_text(text)

    def callbackFinished(self, obj, data=None):
        if self.process==None:
            raise RuntimeError("No worker process started")
        print "all done; joining worker process"
        self.process.join()
        self.process = None

        self.progress.set_fraction(1.0)
        self.progress.set_text("done")

    def go(self, widget, data=None):
        if self.process!=None:
            return

        print "Creating shared Queue"
        queue = multiprocessing.Queue()

        print "Creating Worker"
        worker = Worker(queue)

        print "Creating Listener"
        listener = Listener(queue)
        listener.connect("updated",self.callbackDisplay)
        listener.connect("finished",self.callbackFinished)

        print "Starting Worker"
        self.process = multiprocessing.Process(target=worker.go, args=())
        self.process.start()

        print "Starting Listener"
        thread = threading.Thread(target=listener.go, args=())
        thread.start()

if __name__ == '__main__':
    gui = Interface()
    gui.main()
