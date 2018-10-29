from rallf.tools import Communicator


class Logger(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def debug(self, msg, data=None):
        #print("MENSAJE: %s" % msg)
        return self.log(msg, 0, data)
