import Commands
import socket


class Core():
    def __init__(self):
        self.configFile = open('config.txt', 'r').readlines()
        self.nick = self.configFile[0].split()[1]
        self.host = self.configFile[1].split()[1]
        self.port = int(self.configFile[2].split()[1])
        self.admin = self.configFile[3].split()[1]
        self.chan = self.configFile[4].split()[1]
        self.ident = self.nick
        self.realname = self.nick
        try:
            self.passwd = self.configFile[5].split()[1]
        except IndexError:
            self.passwd = None
        socket.socket = socket.socket()
        socket.socket.connect((self.host, self.port))
        socket.socket.send('nick '+self.nick+'\r\n')
        socket.socket.send('USER '+self.ident+' '+self.host+' derp :'+self.realname+'\r\n')
        if self.passwd != None:
            socket.socket.send('PRIVMSG NickServ identify '+self.passwd+'\r\n')
        socket.socket.send('JOIN '+self.chan+'\r\n')
        
    def Run(self):
        ret = ''
        join = True
        while ret != 'quit':
            commands = Commands.Commands(self.chan, self.nick, self.admin)
            if join == True:
                commands.Log(self.nick, 'joined '+self.chan)
                join = False
            ret = commands.Run()
            if (ret != 'quit'):
                reload(Commands)
                commands.SayReloaded()

core = Core()
core.Run()
socket.socket.shutdown(socket.SHUT_RDWR)
socket.socket.close()
