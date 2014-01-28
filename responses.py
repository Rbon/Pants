"""Todo:

Add admin commands.
"""

class Phrase(object):
    def __init__(self, keys, replies):
        self.keys = keys
        self.replies = replies
        Responses.phrases.append(self)

class Responses(object):
    def __init__(self, pants):
        self.pants = pants
        self.phrases = []
        Phrase(
            ["foo"],
            ["bar","Test successful."]
        )
        Phrase(
            ["tell me a story"],
            [
            "There once was an ugly barnacle. " \
            "It was so ugly that everyone died. The end.",
            "It was a dark and stormy... " \
            "yeah, I'm drawing a blank here.",
            "There was something about ponies... " \
            "I think I'll let jercos tell you.",
            ]
        )

    def parse(self, message):
        self.current_message = message
        if message[0] == "Pants: foo":
            self.send("Yeah, it works.")
        if message[0] == "Pants: poo":
            self.send("shart")
        if message[0] == "Pants: say goodnight":
            self.send("'night.")
        elif message[0] == "Pants: reload":
            if self.current_message[2] == "godofluigi":
                self.pants.reload(current_message[4])
                self.send("Reloaded.")
            else:
                self.send("Sorry {}, you don't have permission.".format(
                    self.current_message[1]
                    )
                )

    def send(self, message):
        self.pants.send(
            (
                message,
                self.current_message[3],
            ),
            self.current_message[4]
        )


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

        self.storyList = [
            'There once was an ugly barnacle. It was so ugly that everyone died. The end.',
            'It was a dark and stormy night...',
            'There was something about ponies... I think I\'ll let jercos tell you.',
            ]