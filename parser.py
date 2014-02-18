"""Todo:

Make Pants email me every week with messages with his name in them that
didn't match any phrases.
"""


import random
import re


class Responses(object):
    def __init__(self, pants):
        self.pants = pants
        self.message = None
        self.name = "Pants"
        self.phrase = re.compile('\n')
        self.dialog = open("responses.txt", "r").read().splitlines()

        self.tmp_dialog = []
        for line in self.dialog:
            self.tmp_dialog.append(line.strip(' "'))
        self.dialog = self.tmp_dialog

        self.dialog = "\n".join(self.dialog).split("\n\n")

        self.tmp_dialog = []
        for line in self.dialog:
            self.tmp_dialog.append(line.strip("\n").splitlines())
        self.dialog = self.tmp_dialog

        self.tmp_dialog = []
        while self.dialog:
            dialog_line = []
            line = self.dialog.pop()
            dialog_line.append(line)
            line = self.dialog.pop()
            tmp_line = []
            for item in line:
                tmp_line.append(re.compile(item.format(name=self.name)))
            line = tmp_line
            dialog_line.append(line)
            self.tmp_dialog.append(dialog_line)
        self.dialog = self.tmp_dialog

        self.dialog.reverse()

        print self.dialog

    def parse(self, message):
        self.message = message
        for dialog_group in self.dialog:
            for item in dialog_group[1]:
                match = item.search(message[0])
                if match:
                    reply = dialog_group[0][
                        random.randint(0, len(dialog_group[0]) - 1)
                        ]
                    self.send(reply.format(sender=message[1].split()[0]))
                    return
                else:
                    print "no match"
                    

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


    #     for phrase in self.phrases:
    #         phrase_index = self.phrases.index(phrase)
    #         for reply in phrase[0]:
    #             reply_index = phrase[0].index(reply)
    #             self.phrases[phrase_index][0][reply_index] = reply.format(
    #                 name=self.name)


    # def parse(self, message):
    #     self.message = message
    #     if self.name in message[0][0]:
    #         message[0] = message[0].split()
    #         for word in message[0]:
    #             word_index = message[0].index(word)
    #             if not self.name in word:
    #                 message[0][word_index] = word.lower()
    #         message[0] = " ".join(message[0])
    #         message[0] = message[0].rstrip(".?!")
    #     else:
    #         message[0].lower()
        
    #     for phrase in self.phrases:
    #         if message[0] in phrase[0]:
    #             reply = phrase[1][random.randint(0, len(phrase[1]) - 1)]
    #             if type(reply) == str:
    #                 self.send(reply.format(sender=message[1].split()[0]))
    #             else:
    #                 reply()