# -*- coding: utf-8 -*-
import gtk
import locale
import gettext
import os


if __name__ == "__main__":

    #os.environ['LANGUAGE'] = 'en'
    #os.environ['LANG'] = 'en'

    GETTEXT_DOMAIN = "canaimainstalador"
    GETTEXT_LOCALEDIR = os.path.join(os.path.dirname(__file__), 'locale')

    gettext.install(GETTEXT_DOMAIN, GETTEXT_LOCALEDIR)
    #_ = gettext.gettext

    print locale.getlocale()
    print locale.getdefaultlocale()

    print _("Hola")

    lbl = gtk.Label(_('Hola'))
    lbl.set_line_wrap(True)
    lbl.set_alignment(0, 0.5)
    lbl.set_justify(gtk.JUSTIFY_FILL)
    lbl.set_size_request(640, -1)
    lbl.show()

    diag = gtk.Dialog()
    diag.set_resizable(True)
    diag.vbox.pack_start(lbl, True, True, 0)
    diag.run()
