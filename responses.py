"""Todo:

Make Pants email me every week with messages with his name in them that
didn't match any phrases.
"""

import random


class Responses(object):
    def __init__(self, pants):
        self.pants = pants
        self.message = None
        self.name = "Pants"
        self.phrases = [
            (
                [
                    "{name}: calc 2+2"
                ],
                [
                    "Hey man, I'm not a scientist."
                ]
            ),
            (
                [
                    "{name}: botsnack"
                ],
                [
                    "nomnomnom"
                ]
            ),
            (
                [
                    "Pants: tell me a story"
                ],
                [
                    "There once was an ugly barnacle. " \
                    "It was so ugly that everyone died. The end.",
                    "It was a dark and stormy... " \
                    "yeah, I'm drawing a blank here.",
                    "There was something about ponies... " \
                    "I think I'll let jercos tell you."
                ]
            ),
            (
                [
                    "{name}: hello",
                    "{name}: bonjour",
                    "{name}: hi",
                    "{name}: hola",
                    "{name}: sup",
                    "{name}: hey",
                    "hi {name}",
                    "hey {name}"
                ],         
                [   
                    "Hola.",
                    "Heyo.",
                    "Yo.",
                    "Hey {sender}.",
                    "Hey there, {sender}."
                ]
            ),
            (
                [
                    "{name}: explode"
                ],
                [
                    "/me exploded"
                ]
            ),
            (
                [
                    "{name}: reload"
                ],
                [
                    self.reload
                ]
            ),
            (
                [
                    ":D"
                ],
                [
                    ":D"
                ]
            ),
            (
                [
                    "D:"
                ],
                [
                    "D:"
                ]
            ),
            (
                [
                    ">.>"
                ],
                [
                    ">.>"
                ]
            ),
            (
                [
                    "<.<"
                ],
                [
                    "<.<"
                ]
            ),
            (
                [
                    "{name}: >.>"
                ],
                [
                    "{sender}: <.<"
                ]
            ),
            (
                [
                    "{name}: <.<"
                ],
                [
                    "{sender}: >.>"
                ]
            ),
            (
                [
                    ":o"
                ],
                [
                    ":o"
                ]
            ),
            (
                [
                    ":O"
                ],
                [
                    ":O"
                ]
            )
            # (
            #     [
            #         "{name}: "
            #     ],
            #     [
            #         "It is certain.",
            #         "It is decidedly so.",
            #         "Without a doubt.",
            #         "Yes - definitely.",
            #         "You may rely on it.",
            #         "As I see it, yes.",
            #         "Most likely.",
            #         "Outlook good.",
            #         "Signs point to yes.",
            #         "Yes.",
            #         "Reply hazy, try again.",
            #         "Ask again later.",
            #         "Better not tell you now.",
            #         "Cannot predict now.",
            #         "Concentrate and ask again.",
            #         "Don't count on it",
            #         "My reply is no.",
            #         "My sources say no.",
            #         "Outlook not so good.",
            #         "Very doubtful."
            #     ]
            # )
        ]
        for phrase in self.phrases:
            phrase_index = self.phrases.index(phrase)
            for reply in phrase[0]:
                reply_index = phrase[0].index(reply)
                self.phrases[phrase_index][0][reply_index] = reply.format(
                    name=self.name)


    def parse(self, message):
        self.message = message
        if self.name in message[0]:
            message[0] = message[0].split()
            for word in message[0]:
                word_index = message[0].index(word)
                if not self.name in word:
                    message[0][word_index] = word.lower()
            message[0] = " ".join(message[0])
            message[0] = message[0].rstrip(".?!")
        else:
            message[0].lower()
        
        for phrase in self.phrases:
            if message[0] in phrase[0]:
                reply = phrase[1][random.randint(0, len(phrase[1]) - 1)]
                if type(reply) == str:
                    self.send(reply.format(sender=message[1].split()[0]))
                else:
                    reply()

    def reload(self):
        if self.message[2] == "godofluigi":
            self.pants.reload()
            self.send("Reloaded.")
        else:
            self.send("Sorry {}, you don't have permission.".format(
                self.message[1]
                )
            )

    def send(self, message):
        self.pants.send(
            (
                message,
                self.message[3],
            ),
            self.message[4]
        )
