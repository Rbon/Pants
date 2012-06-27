import string
import random
import datetime
import os


class Commands():
    def __init__(self, socket, chan, nick, admin):
        self.socket = socket
        self.admin = admin
        self.nick = nick
        self.chan = chan
        self.message = ''
        self.sender = ''
        self.socketFile = self.socket.makefile()
        self.commandList = {
            'reload' : self.Reload,
            'say': self.Say,
            'quit' : self.Quit,
            }
        self.PONG = ''

        self.quitPhrases = [
            '%s dropped' % (self.nick),
            '%s has been removed' % (self.nick),
            ]
        self.botsnackList = [
            'nomnomnom',
            ]
        self.helloList = [
            'Hola.',
            'Heyo.',
            'Yo.',
            'Hey __SENDER__.',
            'Hey there, __SENDER__.',
            ]
        self.explodeList = [
            '\x01ACTION exploded\x01',
            ]
        self.storyList = [
            'There once was an ugly barnacle. It was so ugly that everyone died. The end.',
            'It was a dark and stormy night...',
            'There was something about ponies... I think I\'ll let jercos tell you.',
            ]
        self.lonelyList = [
            '...with my mouth?',
            ]
        self.eyeList = [
            '__SENDER__: <.<',
            ]
        self.dropList = [
            '\x01ACTION dropped it like it\'s hot\x01'
            ]
        self.eightBallList = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Signs point to yes.',
            'Yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.',
            ]
        self.danceList = [
            '\x01ACTION does the Pants Dance',
            ]
        self.testList = [
            'I lik-a do da cha cha.',
            ]
        #list of commands
        self.responseList = {
            'dance':self.danceList,
            'botsnack':self.botsnackList,
            'hello':self.helloList,
            'hello.':self.helloList,
            'hello?':self.helloList,
            'hi':self.helloList,
            'hola':self.helloList,
            'aloha':self.helloList,
            'yo':self.helloList,
            'explode':self.explodeList,
            'tell me a story':self.storyList,
            'make me not lonely':self.lonelyList,
            '>.>':self.eyeList,
            'drop':self.dropList,
            'test':self.testList,
            }

    def Run(self):
        running = None
        while running == None:
            self.chat = self.socketFile.readline()
            self.now = datetime.datetime.today()
            self.AltLog(self.chat)
            if self.chat.find('PING') == 0:
                self.PONG = self.chat[self.chat.find('PING')+4:]
                self.socket.send('PONG' + self.PONG)
##                self.AltLog('SENT PONG'+self.PONG)
            self.sender = self.chat[1:self.chat.find('!')]
            self.message = self.chat[self.chat.find(self.chan) + len(self.chan) + 2:len(self.chat) - 2]
            if self.chat.find('PRIVMSG') != -1:
                self.Log(self.sender, self.message)
                if self.message.find(self.nick+': ') == 0:
                    self.message = self.message[len(self.nick) + 2 : ]
                    try:
                        command = self.message.lower().split()[0]
                        token = self.message[len(command) : ]
                        running = self.commandList[command](token)
                    except KeyError:
                        if self.responseList.has_key(self.message):
                            self.Respond(self.message)
                        #check for a question mark
                        elif command.find('?') != -1:
                            try:
                                randomLen = len(self.eightBallList)-1
                                exactResponse = self.eightBallList[random.randint(0, randomLen)]
                                self.Send(exactResponse)
                            except KeyError:
                                    return      
                    except TypeError:
                        running = self.commandList[command]()
            elif self.chat.find('NOTICE') == -1:
                if self.chat.find('JOIN')!=-1:
                    self.Log(self.sender, '\x01ACTION joined '+self.chan)
                elif self.chat.find('QUIT')!=-1:
                    messageStart = self.chat.find('QUIT') + 5
                    if self.chat.find(':Quit:') != -1:
                        messageStart += 7
                    self.message = self.chat[messageStart:]
                    self.Log(self.sender, '\x01ACTION quit '+self.chan+': '+self.message)
                elif self.chat.find('PART')!=-1:
                    self.Log(self.sender, '\x01ACTION parted '+self.chan+': '+self.message)
                elif self.chat.find('ACTION') != -1:
                    self.message=chat[messageStart+len(self.chan)+10:]
                    self.Log(self.sender,self.message[0:len(self.message)-2])
        return running

    def Respond(self, token):
        response = self.responseList[token]
        randomLen = len(response)-1
        exactResponse = response[random.randint(0, randomLen)]
        exactResponse = exactResponse.replace('__SENDER__', self.sender)
        self.Send(exactResponse)

    #This is as far as I got in remaking Log. 
##    def Log(self, token, parse = False, fileName = 'log.txt'):
##        token = token.rstrip(string.whitespace)
##        if parse == True:
##            output = ''
##            log = ''
##            blackList = [
##                'PING',
##                self.chan,
##                self.nick,
##                ]
##            splitToken = token.split()
##            if blackList.HAS THING(splitToken[0]):
##                print 'IT IS IN'
##                if splitToken[1] == 'PRIVMSG':
##                    if splitToken[3] == ':\x01ACTION':
##                        message = token[token.find(':\x01ACTION') + 9:]
##                    else:
##                        sender = '<'+self.sender+'>'
##                        message = token[token.find(' :') + 2:]
##                    log = sender+' '+message
##                if splitToken[1] == 'QUIT':
##                    message = token[token.find('QUIT')+5]
##                    if splitToken[2] == ':Quit:':
##                        message = message[7:]
##                    log = self.sender+' quit '+self.chan+' '+message
##                output = self.now.strftime('[%Y-%m-%d][%H:%M]')+' '+log
##        else:
##            output = token
##        logFile = open(fileName, 'a')
##        logFile.write(output+'\n')
##        logFile.close()
##        print output

    def Log(self, sender, message):
        if message.find('\x01ACTION ') == 0:
            message = message[8:]
        else:
            sender = '<'+sender+'>'
        self.now = datetime.datetime.today()
        line = self.now.strftime('[%Y-%m-%d][%H:%M]')+' '+sender+' '+message.rstrip(string.whitespace)
        self.logFile = open('log.txt', 'a')
        self.logFile.write(line+'\n')
        self.logFile.close()
        print line

    def AltLog(self, message):
        if message != '':
            logFile = open('altlog.txt', 'a')
            logFile.write(message)
            logFile.close()

    def Say(self, token):
        self.Send(token.strip())

    def SayReloaded(self):
        self.Send('Done.')

    def Reload(self):
        if self.sender == self.admin:
            os.system('git pull git://github.com/Rbon/Pants.git master')
            return False
        else:
            self.Send(self.sender + ': you don\'t have permission, dude.')
        
    def Send(self, token):
        self.Log(self.nick, token)
        #Part of the unfinished Log
##        if token.endswith('\x01'):
##            self.Log(self.now.strftime('[%Y-%m-%d][%H:%M]')+' '+self.nick+' '+token[8:])
##        else:
##            self.Log(self.now.strftime('[%Y-%m-%d][%H:%M]')+' <'+self.nick+'> '+token)
        self.socket.send('PRIVMSG %s :%s\r\n' % (self.chan, token))

    def Quit(self):
        if self.sender == self.admin:
            randomLen = len(self.quitPhrases)-1
            exactResponse = self.quitPhrases[random.randint(0, randomLen)]
            quitResponse = 'QUIT :'+exactResponse+'\r\n'
            self.socket.send(quitResponse)
            self.Log(self.nick, 'quit '+self.chan+': '+exactResponse)
            return 'quit'
        else:
            self.Send(self.sender + ': you don\'t have permission, dude.')

 
