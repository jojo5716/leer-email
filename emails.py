# -*- coding: utf-8 -*-
import sys
import gtk
import imaplib
import pynotify
from email.header import decode_header
from email.parser import Parser


class Email(object):
    def __init__(self):
        self.HOST = 'imap.gmail.com'
        self.PORT = 993
        self.email = ""
        self.password = ""
        self.ETIQUETA = "" # Etiqueta de gmail a leer


        if not pynotify.init("Notificaciones"):
            print "Ha fallado al iniciar las notificaciones"
            sys.exit(1)

    def lanza_mensaje(self, titulo, mensaje=""):
        pynotify.Notification(titulo,
                              mensaje,
                              icon=gtk.STOCK_DIALOG_INFO).show()

    def obtenemos_cliente(self):
        client =  imaplib.IMAP4_SSL(self.HOST, self.PORT)
        if not client.login(self.email, self.password):
            # Ha fallado el login
            sys.exit(1)
        return client

    def obtenemos_email(self):
        client = self.obtenemos_cliente()
        estado, data = client.select(self.ETIQUETA)
        if estado != 'OK':
            titulo = "No existe la etiqueta seleccionada"
            self.lanza_mensaje(titulo)
            sys.exit(1)

        estado, data = client.search(None, '(UNSEEN)')
        if estado == 'OK' and data[0] != '':
            for msg_id in sorted(data[0].split()):
                if msg_id != '':
                    estado, data = client.fetch(msg_id, '(RFC822)')
                    if estado == 'OK':
                        msg = Parser().parsestr(data[0][1])
                        titulo = self.obtenemos_header(msg, 'From')
                        mensaje = self.obtenemos_header(msg, 'Subject')
                        self.lanza_mensaje(titulo, mensaje)
        else:
            titulo = "Ya has visto todos tus emails"
            self.lanza_mensaje(titulo)

    def obtenemos_header(self, msg, header):
        header = decode_header(msg.get(header))
        if (header[0][1]):
            return unicode(header[0][0], header[0][1]).encode('utf8')
        else:
            return header[0][0]


if __name__ == "__main__":
    e = Email()
    e.obtenemos_email()
