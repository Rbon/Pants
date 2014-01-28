"""Todo:

Add admin commands.
"""

import random


class Responses(object):
    def __init__(self, pants):
        self.pants = pants
        self.message = None
        self.phrases = [
            (
                [
                    "Pants: foo",
                    "Pants: bar"
                ],
                [
                    "Test successful."
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
                    "Pants: hello"
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
                    "Pants: test"
                ],
                [
                    self.test
                ]
            ),
            (
                [
                    "Pants: explode"
                ],
                [
                    "/me exploded"
                ]
            )
        ]

    def parse(self, message):
        self.message = message
        if message[0] == "Pants: reload":
            if self.message[2] == "godofluigi":
                self.pants.reload()
                self.send("Reloaded.")
            else:
                self.send("Sorry {}, you don't have permission.".format(
                    self.message[1]
                    )
                )
        for phrase in self.phrases:
            if message[0] in phrase[0]:
                reply = phrase[1][random.randint(0, len(phrase[1]) - 1)]
                if type(reply) == str:
                    self.send(reply.format(sender=message[1].split()[0]))
                else:
                    print reply
                    reply()


    def send(self, message):
        self.pants.send(
            (
                message,
                self.message[3],
            ),
            self.message[4]
        )


    def test(self):
        self.send("This is a test.")

        # self.eightBallList = [
        #     'It is certain.',
        #     'It is decidedly so.',
        #     'Without a doubt.',
        #     'Yes - definitely.',
        #     'You may rely on it.',
        #     'As I see it, yes.',
        #     'Most likely.',
        #     'Outlook good.',
        #     'Signs point to yes.',
        #     'Yes.',
        #     'Reply hazy, try again.',
        #     'Ask again later.',
        #     'Better not tell you now.',
        #     'Cannot predict now.',
        #     'Concentrate and ask again.',
        #     'Don\'t count on it',
        #     'My reply is no.',
        #     'My sources say no.',
        #     'Outlook not so good.',
        #     'Very doubtful.',
        #     ]
