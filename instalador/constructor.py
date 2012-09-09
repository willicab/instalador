#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def aconnect(button, signals, function, params):
    '''
        desconecta los eventos existentes en signals y conecta con function
    '''
    for i in signals:
        if button.handler_is_connected(i):
            button.disconnect(i)
    signals.append(button.connect_object('clicked', function, params))

    return signals

def msg_error(mensaje):
    '''
        Función que muestra el mensaje de error
    '''
    dialog = gtk.MessageDialog(wizard,
         gtk.DIALOG_MODAL,
         gtk.MESSAGE_ERROR,
         gtk.BUTTONS_OK,
         mensaje)
    response = dialog.run()
    dialog.destroy()

def UserMessage(message, title, mtype, buttons,
                    c_1 = False, f_1 = False, p_1 = '',
                    c_2 = False, f_2 = False, p_2 = '',
                    c_3 = False, f_3 = False, p_3 = ''
                    ):

    dialog = gtk.MessageDialog(
        parent = None, flags = 0, type = mtype,
        buttons = buttons, message_format = message
        )
    dialog.set_title(title)
    response = dialog.run()
    dialog.destroy()

    if response == c_1:
        f_1(*p_1)
    if response == c_2:
        f_2(*p_2)
    if response == c_3:
        f_3(*p_3)

    return response
