from rallf.tools import Communicator


class Caller(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def use(self, routine, args):
        return self.rpccall("delegate_local", routine, args)

    def delegate(self, routine, args):
        return self.rpccall("delegate_remote", routine, args)
