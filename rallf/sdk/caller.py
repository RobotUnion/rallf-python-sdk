from rallf.tools.communicator import Communicator


class Caller(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def call(self, type, routine, args):
        return self.rpccall(type, {"routine": routine, "params": args}, random.randint(0, 30000))

    def use(self, routine, args):
        return self.call("delegate_local", routine, args)

    def delegate(self, routine, args):
        return self.call("delegate_remote", routine, args)
