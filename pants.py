import datetime
import os
import time

import parser
import skype


class Pants(object):
    def __init__(self):
        super(Pants, self).__init__()
        self.responses = parser.Responses(self)
        self.skype = skype.Skype(self)
        self.protocols = {"skype": self.skype}
        self.old_responses = None

    def parse(self, message):
        self.output("{0}: {1}".format(
            message[1],
            message[0]
            )
        )
        self.responses.parse(message)

    def log(self, message):
        log_file = open("log.txt", "a")
        log_file.write(message+"\n")
        log_file.close()

    def output(self, message):
        output = "{0} {1}".format(
            datetime.datetime.today().strftime("[%Y-%m-%d %H:%M:%S]"),
            message
            )
        self.log(output)
        print output

    def send(self, message, protocol):
        self.protocols[protocol].send(message)
        self.output("Pants: {}".format(message[0]))

    def reload(self):
        os.system("git pull git://github.com/Rbon/Pants.git master")
        reload(responses)
        self.responses = responses.Responses(self)

    def run(self):
        while True:
            try:
                time.sleep(1.0)
            except KeyboardInterrupt:
                print "\nQuitting."
                quit()

             
if __name__ == "__main__":
    pants = Pants().run()
