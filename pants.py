#Pants: a chatbot by Rbon.

#TODO:
#add hot-loading
#make the check for beginning of message easier to copy

import socket
import string
import random
import time
import datetime

host = "mindjail.subluminal.net"
port = 6667
nick = "Pants"
ident = "Pants"
realname = "Pants"
chan = "#thoseguys"
admin = "Rbon"

dColon = 0
colonD = 0

def send(message):
    log(nick, message)
    s.send("PRIVMSG "+chan+" :"+message+"\r\n")

def log(sender, message):
    if message.find("\x01ACTION ") == 0:
        message = message[8:]
    else:
        sender = "<"+sender+">"
    now = datetime.datetime.today()
    print "["+now.strftime("%H:%M")+"] "+sender+" "+message
    return

def ponies():
        s.send("PRIVMSG %s :Warning: may contain ponies.\r\n" % (chan))
        log(nick, "Warning: may contain ponies.")
        return

s=socket.socket( )
s.connect((host, port))
s.send("nick %s\r\n" % (nick))
s.send("USER %s %s bla :%s\r\n" % (ident, host, realname))
s.send("JOIN %s\r\n" % (chan))
log(nick,"\x01ACTION joined "+chan)

while 1:
    chat=s.makefile().readline()
    nickEnd = chat.find("!")
    sender = chat[1:nickEnd]
    messageStart = chat.find("%s :" % (chan))
    message = chat[messageStart+len(chan)+2:]

    if chat[0:4]=="PING":
        s.send("PONG"+chat[4:])
        log("NOTICE", "GOT PING: '%s'" % (chat))
        log("NOTICE", "SENT PING: '%s'" %(chat[4:]))
    
    if chat.find("PRIVMSG")== -1:
        if chat.find("NOTICE") == -1:
            if chat.find("JOIN")!=-1:
                log(sender, "\x01ACTION joined "+chan)
            elif chat.find("QUIT")!=-1:
                messageStart=chat.find(":Quit:")+7
                message = chat[messageStart:]
                log(sender, "\x01ACTION quit "+chan+": "+message)
            elif chat.find("PART")!=-1:
                log(sender, "\x01ACTION parted "+chan+": "+message)
            elif chat.find("ACTION") != -1:
                message=chat[messageStart+len(chan)+10:]
                log(sender,message[0:len(message)-2])
    elif chat.find("PRIVMSG") != -1:
        log(sender,message[0:len(message)-2])

    quitPhrases = ["%s dropped" % (nick),
                   "%s has been removed" % (nick)]
    
    botsnackList = [
        "nomnomnom",
        ]
    
    helloList = [
        "Hola.",
        "Heyo.",
        "Yo.",
        "Hey %s." % (sender),
        "Hey there, %s." % (sender),
        ]
    
    explodeList = [
        "\x01ACTION exploded\x01",
        ]
    
    storyList = [
        "There once was an ugly barnacle. It was so ugly that everyone died. The end.",
        "It was a dark and stormy night...",
        "There was something about ponies... I think I'll let jercos tell you.",
        ]
    
    lonelyList = [
        "...with my mouth?",
        ]

    eyeList = [
        "<.<",
        ]

    dropList = [
        "\x01ACTION dropped it like it's hot\x01"
        ]
    
    commandList = {
        "botsnack":botsnackList,
        "hello":helloList,
        "hello.":helloList,
        "hi":helloList,
        "hola":helloList,
        "aloha":helloList,
        "yo":helloList,
        "explode":explodeList,
        "tell me a story":storyList,
        "make me not lonely":lonelyList,
        ">.>":eyeList,
        "drop":dropList,
        }
    
    #admin triggered commands
    if chat.find(":%s!" % (admin))==0:
        if chat.find("%s: quit" % (nick)) != -1:
            quitMessage=quitPhrases[random.randint(0, len(quitPhrases)-1)]
            s.send("QUIT :%s\r\n" % (quitMessage))
            log(nick, "quit "+chan+": "+quitMessage)
            quit(0)
            
    #jercos triggered commands
    if chat.find(":jercos!") == 0:
        if chat.find("http://") != -1:
            if chat.find(".gov") == -1:
                ponies()
        
    #hilight triggered commands
    if chat.find("PRIVMSG") != -1:
        if chat.find("%s:" % (nick)) != -1:
            messageStart = chat.find("%s :" % (chan))
            nickStart = chat.find('%s:' % (nick))
            if messageStart+len(chan)+2 == nickStart:
                command = chat[nickStart+len(nick)+2:].strip().lower()
                #"say" command
                if command.find("say ") != -1:
                    sayBegin = command.find("say")
                    command = chat[nickStart+len(nick)+2:].strip()
                    sayCommand = command[sayBegin+3:].strip()
                    send(sayCommand)
                else:
                    try:
                        response = commandList[command]
                        randomLen = len(response)-1
                        exactResponse = response[random.randint(0, randomLen)]
                        send(exactResponse)
                    except KeyError:
                        continue
                    
    #misc. responses
    if chat.find(" D: ") != -1:
        dColon += 2
    elif chat.find(":D: ") != -1:
        dColon += 2
    elif chat.find(" D:\r\n") != -1:
        dColon += 2
    elif chat.find(":D:\r\n") != -1:
        dColon += 2
        
    dColon -= 1
    if dColon < 0:
        dColon = 0
    elif dColon > 1:
        send("D:")
        dColon = 0
        
    if chat.find(" :D ") != -1:
        colonD += 2
    elif chat.find("::D ") != -1:
        colonD += 2
    elif chat.find(" :D\r\n") != -1:
        colonD += 2
    elif chat.find("::D\r\n") != -1:
        colonD += 2
    colonD -= 1
    
    if colonD < 0:
        colonD = 0
    elif colonD > 1:
        send(":D")
        colonD = 0

    message = message.lower()
    if message.find("shepard\r\n") != -1:
        send("Wrex.")
    elif message.find("shepard.\r\n") != -1:
        send("Wrex.")
