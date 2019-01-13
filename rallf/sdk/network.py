from rallf.tools.communicator import Communicator


class Network(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def call(self, kind, routine, args):
        return self.rpccall(kind, {"routine": routine, "params": args})

    def use(self, routine, args=None):
        return self.call("delegate_local", routine, args)

    def delegate(self, routine, args=None):
        return self.call("delegate_remote", routine, args)

    def event(self, name, data=None):
        return self.rpccall("event", {"name": name, "data": data}, wait=False)
