from rallf.tools import Communicator


class Logger:
    def __init__(self, input, output):
        super().__init__(input, output)

    def debug(self, msg, data=None):
        return self.log(msg, 0, data)
