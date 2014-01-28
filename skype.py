import Skype4Py

class Skype(object):
    def __init__(self, pants):
        self.pants = pants
        self.ignored_statuses = ["READ", "SENDING", "SENT"]
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()

    def MessageStatus(self, Message, Status):
        if not Status in self.ignored_statuses:
            Message.MarkAsSeen()
            self.pants.parse(
                (
                    Message.Body,
                    Message.Sender.FullName,
                    Message.Sender.Handle,
                    Message.Chat,
                    "skype"
                )
            )

    def send(self, message):
        message[1].SendMessage(message[0])