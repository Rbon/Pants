#Pants: a chatbot by Rbon.

#TODO:
#make it send a manual PONG after three minutes
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

#things that need to be set beforehand
dColon = 0
colonD = 0
pingTime = time.time()
PONG = ""

def send(message):
    log(nick, message)
    s.send("PRIVMSG %s :%s\r\n" % (chan, message))

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

    #responces to commands
    quitPhrases = [
        "%s dropped" % (nick),
        "%s has been removed" % (nick),
        ]
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
        sender+": <.<",
        ]
    dropList = [
        "\x01ACTION dropped it like it's hot\x01"
        ]
    eightBallList = [
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
    commandList = {
        "botsnack":botsnackList,
        "hello":helloList,
        "hello.":helloList,
        "hello?":helloList,
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


    #pony related things
    ponyWhiteList = [
        ".gov",
        "wikipedia.org",
        "ebay.com",
        "pastebin.com",
        "snag.gy",
        "4chanarchive.org",
        ]

    ponyBlackList = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        "tumbler.com",
        "youtube.com",
        "youtu.be",
        "snag.gy",
        "imgur.com",
        ]

    if chat.find("PING") != -1:
        PONG = chat[chat.find("PING")+4:]
        s.send("PONG%s" % (PONG))
        log("NOTICE", "GOT:  %s" % (chat[:-2]))
        log("NOTICE", "SENT: PONG%s" % (PONG[:-2]))
        pingTime = time.time()

    nowTime = time.time()
    if nowTime - pingTime > 180:
        s.send("PONG%s" % (PONG))
        log("NOTICE", "NO PING IN 3 MINUTES")
        log("NOTICE", "SENT: PONG%s" % (PONG[:-2]))
        pingTime = time.time()
    
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
            
        #jercos triggered commands
        #if sender == "jercos":
        #    if chat.find("http://") != -1:
        #        line = chat.lower()
        #        for item in ponyBlackList:
        #            if line.find(item) != -1:
        #                ponies()
        #                break

        #hilight triggered commands
        if chat.find("%s:" % (nick)) != -1:
            messageStart = chat.find("%s :" % (chan))
            nickStart = chat.find('%s:' % (nick))
            if messageStart+len(chan)+2 == nickStart:
                command = chat[nickStart+len(nick)+2:].strip().lower()

                #check for a generic command
                try:
                    response = commandList[command]
                    randomLen = len(response)-1
                    exactResponse = response[random.randint(0, randomLen)]
                    send(exactResponse)
                except KeyError:
                    
                    #admin triggered commands
                    if chat.find(":%s!" % (admin))==0:
                        if chat.find("quit") != -1:
                            quitMessage=quitPhrases[random.randint(0, len(quitPhrases)-1)]
                            s.send("QUIT :%s\r\n" % (quitMessage))
                            log(nick, "quit "+chan+": "+quitMessage)
                            quit(0)
                            
                    #check for "say" command
                    if command.find("say ") != -1:
                        sayBegin = command.find("say")
                        command = chat[nickStart+len(nick)+2:].strip()
                        sayCommand = command[sayBegin+3:].strip()
                        send(sayCommand)
                        
                    #check for a question mark
                    elif command.find("?") != -1:
                        try:
                            randomLen = len(eightBallList)-1
                            exactResponse = eightBallList[random.randint(0, randomLen)]
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


