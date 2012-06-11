import string
import random
import time
import datetime
import sys
import warnings


class Commands():
    def __init__(self, socket, chan, nick, admin):
        self.admin = admin
        self.nick = nick
        self.chan = chan
        self.socket = socket
        self.message = ''
        self.sender = ''
        self.chat = ''
        self.dColon = 0
        self.colonD = 0
        
        self.commandList = {
            'reload' : self.Reload,
            'quit' : self.Quit,
            }
        self.pingTime = time.time()
        self.PONG = ''

        self.quitPhrases = [
            "%s dropped" % (self.nick),
            "%s has been removed" % (self.nick),
            ]
        self.botsnackList = [
            "nomnomnom",
            ]
        self.helloList = [
            "Hola.",
            "Heyo.",
            "Yo.",
            "Hey __SENDER__.",
            "Hey there, __SENDER__.",
            ]
        self.explodeList = [
            "\x01ACTION exploded\x01",
            ]
        self.storyList = [
            "There once was an ugly barnacle. It was so ugly that everyone died. The end.",
            "It was a dark and stormy night...",
            "There was something about ponies... I think I'll let jercos tell you.",
            ]
        self.lonelyList = [
            "...with my mouth?",
            ]
        self.eyeList = [
            self.sender+": <.<",
            ]
        self.dropList = [
            "\x01ACTION dropped it like it's hot\x01"
            ]
        self.eightBallList = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
            "Yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            ]
        #list of commands
        self.responseList = {
            "botsnack":self.botsnackList,
            "hello":self.helloList,
            "hello.":self.helloList,
            "hello?":self.helloList,
            "hi":self.helloList,
            "hola":self.helloList,
            "aloha":self.helloList,
            "yo":self.helloList,
            "explode":self.explodeList,
            "tell me a story":self.storyList,
            "make me not lonely":self.lonelyList,
            ">.>":self.eyeList,
            "drop":self.dropList,
            }

    def Run(self):
        running = None
        while running == None:
            self.now = time.time()
            self.chat = self.socket.makefile().readline()
            print self.chat
            if self.chat.find('PING') == 0:
                self.PONG = self.chat[self.chat.find('PING')+4:]
                self.socket.send('PONG' + self.PONG)
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
                        if self.responseList.has_key(command):
                            self.Respond(command)
                            #check for a question mark
                        elif command.find("?") != -1:
                            try:
                                randomLen = len(self.eightBallList)-1
                                exactResponse = self.eightBallList[random.randint(0, randomLen)]
                                self.Send(exactResponse)
                            except KeyError:
                                    return
                                        
                    except TypeError:
                        running = self.commandList[command]()
            elif self.chat.find("NOTICE") == -1:
                if self.chat.find("JOIN")!=-1:
                    self.Log(self.sender, "\x01ACTION joined "+self.chan)
                elif self.chat.find("QUIT")!=-1:
                    messageStart=self.chat.find(":Quit:")+7
                    self.message = self.chat[messageStart:]
                    self.Log(self.sender, "\x01ACTION quit "+self.chan+": "+self.message)
                elif self.chat.find("PART")!=-1:
                    self.Log(self.sender, "\x01ACTION parted "+self.chan+": "+self.message)
                elif self.chat.find("ACTION") != -1:
                    self.message=chat[messageStart+len(self.chan)+10:]
                    self.Log(self.sender,self.message[0:len(self.message)-2])
        return running

    def Respond(self, token):
        response = self.responseList[token]
        randomLen = len(response)-1
        exactResponse = response[random.randint(0, randomLen)]
        exactResponse = exactResponse.replace('__SENDER__', self.sender)
        self.Send(exactResponse)

    def Log(self, sender, message):
        if message.find("\x01ACTION ") == 0:
            message = message[8:]
        else:
            sender = "<"+sender+">"
        self.now = datetime.datetime.today()
        print "["+self.now.strftime("%H:%M")+"] "+sender+" "+message


    def Say(self, token):
        self.Send(token)

    def SayReloaded(self):
        self.Send('Done.')

    def Reload(self):
        self.Send('Reloading...')
        return False
        
    def Send(self, token):
        self.Log(self.nick, token)
        self.socket.send('PRIVMSG %s :%s\r\n' % (self.chan, token))

    def Quit(self):
        if self.sender == self.admin:
            randomLen = len(self.quitPhrases)-1
            exactResponse = self.quitPhrases[random.randint(0, randomLen)]
            quitResponse = 'QUIT :'+exactResponse+'\r\n'
            self.socket.send(quitResponse)
            self.Log(self.nick, "quit "+self.chan+": "+exactResponse)
            return 'quit'
        else:
            self.Send(self.sender + ': you don\'t have permission, dude.')

 
