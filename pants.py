import Commands
import socket


class Core():
    def __init__(self):
        self.host = 'mindjail.subluminal.net'
        self.port = 6667
        self.nick = 'testPants'
        self.ident = 'Pants'
        self.realname = 'Pants'
        self.chan = '#sandbots'
        self.admin = 'Rbon'
        self.socket = None

    
    def Run(self):
        ret = ''
        while ret != 'quit':
            commands = Commands.Commands(self.socket, self.chan, self.nick, self.admin)
            ret = commands.Run()
            if (ret != 'quit'):
                reload(Commands)
                commands.SayReloaded()

    def OpenSocket(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.send('nick %s\r\n' % (self.nick))
        self.socket.send('USER %s %s bla :%s\r\n' % (self.ident, self.host, self.realname))
        self.socket.send('JOIN %s\r\n' % (self.chan))


core = Core()
core.OpenSocket()
core.Run()
core.socket.shutdown(socket.SHUT_RDWR)
core.socket.close()
