#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst
import time

class WebCam:
    def __init__(self, padre):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Imagen de usuario")
        self.window.set_decorated(False)
        self.window.set_default_size(260, 232)
        self.window.connect("destroy", gtk.main_quit, "WM destroy")
        self.padre = padre
        vbox = gtk.Fixed()
        self.window.add(vbox)
        self.movie_window = gtk.DrawingArea()
        self.movie_window.set_size_request(260, 200)
        vbox.put(self.movie_window, 0, 0)
        hbox = gtk.HBox()
        hbox.set_size_request(260, 32)
        vbox.put(hbox, 0, 200)

        self.button3 = gtk.Button("Capturar imagen")
        self.button3.connect("clicked", self.take_snapshot)
        hbox.pack_start(self.button3, True)

        # Set up the gstreamer pipeline
        
        self.player = gst.parse_launch ("v4l2src ! autovideosink")
        #self.player = gst.parse_launch ("v4l2src ! videorate ! video/x-raw-yuv,framerate=30/1,width=320,height=240 ! tee name=t_vid ! queue ! videoflip method=horizontal-flip ! xvimagesink sync=false t_vid. ! queue ! mux. alsasrc ! audio/x-raw-int,rate=48000,channels=2,depth=16 ! queue ! audioconvert ! queue ! mux. avimux name=mux")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

        self.window.set_border_width(3)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.show_all()
        
        self.start_stop(None)
        gtk.gdk.threads_init()
        time.sleep(0.1)
        gtk.main()
        
    def take_snapshot(self,widget):
        img = gtk.gdk.Pixbuf( gtk.gdk.COLORSPACE_RGB, True, 8, 260, 200 )
        image = img.get_from_drawable(self.movie_window.window, 
                                      self.movie_window.window.get_colormap(), 
                                      0, 
                                      0, 
                                      0, 
                                      0, 
                                      260, 
                                      200)
        cropped_buffer = image.subpixbuf(30, 0, 200, 200)
        print cropped_buffer
        pixbuf = cropped_buffer.scale_simple(92, 92, gtk.gdk.INTERP_BILINEAR)
        if (pixbuf != None):
            homedir = "/tmp/face" #os.path.expanduser("~") + "/.face"
            pixbuf.save(homedir,"png")
            self.padre.visor.execute_script("document.getElementById('avatar').src = '{0}?' + new Date();".format(homedir))
            self.padre.face = homedir
            print "Screenshot saved to screenshot.png."
        else:
            print "Unable to get the screenshot."
        self.exit()

    def start_stop(self, w=None):
        #if self.button.get_label() == "Start":
            #self.button.set_label("Stop")
        self.player.set_state(gst.STATE_PLAYING)
        #else:
        #    self.player.set_state(gst.STATE_NULL)
            #self.button.set_label("Start")

    def exit(self, widget=None, data=None):
        self.player.set_state(gst.STATE_NULL)
        gtk.gdk.threads_leave()
        self.window.destroy()
        #gtk.main_quit()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            #self.button.set_label("Start")
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)
            self.msg_error("No se ha encontrado ninguna cámara\n- Error: %s" % err)
            self.exit()
            #self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.movie_window.window.xid)

    def msg_error(self, mensaje):
        '''
            Función que muestra el mensaje de error
        '''
        dialog = gtk.MessageDialog(None,
             gtk.DIALOG_MODAL,
             gtk.MESSAGE_ERROR,
             gtk.BUTTONS_OK,
             mensaje)
        response = dialog.run()
        dialog.destroy()
        
if __name__ == "__main__":
    try:
        a = WebCam()
    except KeyboardInterrupt:
        pass    
