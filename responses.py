"""Todo:

Add admin commands.
"""


class Responses(object):
    def __init__(self, pants):
        self.pants = pants
        self.phrases = {

        }

    def parse(self, message):
        self.current_message = message
        if message[0] == "Pants: foo":
            self.send("fart")
        if message[0] == "Pants: poo":
            self.send("shart")
        if message[0] == "Pants: say goodnight":
            self.send("'night.")
        elif message[0] == "Pants: reload":
            if self.current_message[2] == "godofluigi":
                self.pants.reload()
                self.send("Reloaded.")
            else:
                self.send("Sorry {}, you don't have permission.".format(
                    self.current_message[2]
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
             