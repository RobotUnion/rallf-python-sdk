import time

from rallf.tools.communicator import Communicator


class Network(Communicator):
    def __init__(self, input, output, context):
        super().__init__(input, output)
        self.context = context

    def call(self, routing, target, routine, args):
        return self.rpccall("delegate", {"routing": routing, "target": target, "method": routine, "params": args})

    def use(self, routine, target, args=None):
        return self.call("local", target, routine, args)

    def delegate(self, routine, target, args=None):
        return self.call("remote", target, routine, args)

    def event(self, name, content=None):
        return self.rpccall("event", {"name": name, "context": self.context, "time": "%.9f" % time.time(), "content": content}, wait=False)
