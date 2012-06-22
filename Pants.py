import Commands
import socket


class Core():
    def __init__(self):
        configFile = open('config.txt', 'r').readlines()
        self.nick = configFile[0][configFile[0].find('=')+1:].strip(' \n')
        self.host = configFile[1][configFile[1].find('=')+1:].strip(' \n')
        self.port = int(configFile[2][configFile[2].find('=')+1:].strip(' \n'))
        self.admin = configFile[3][configFile[3].find('=')+1:].strip(' \n')
        self.chan = configFile[4][configFile[4].find('=')+1:].strip(' \n')
        self.ident = self.nick
        self.realname = self.nick
        self.passwd = configFile[5][configFile[5].find('=')+1:].strip(' \n')
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        self.socket.send('nick '+self.nick+'\r\n')
        self.socket.send('USER '+self.ident+' '+self.host+' derp :'+self.realname+'\r\n')
        if self.passwd != '':
            self.socket.send('PRIVMSG NickServ identify '+self.passwd+'\r\n')
        self.socket.send('JOIN '+self.chan+'\r\n')
        
    def Run(self):
        ret = ''
        join = True
        while ret != 'quit':
            commands = Commands.Commands(self.socket, self.chan, self.nick, self.admin)
            if join == True:
                commands.Log(self.nick, 'joined '+self.chan)
                join = False
            ret = commands.Run()
            if (ret != 'quit'):
                reload(Commands)
                commands.SayReloaded()

core = Core()
core.Run()
core.socket.shutdown(socket.SHUT_RDWR)
core.socket.close()
