import json

from rallf.sdk.rallf_error import RallfError
from rallf.tools.communicator import Communicator


class Listener(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def listen(self, task):
        while True:
            req = self.wait()
            if 'method' in req:
                try:
                    resp = getattr(task, req['params']['routine'])(req['params']['args'])
                    task.caller.rpcresponse(req['id'], result=resp, error=False)
                except RallfError as e:
                    task.caller.rpcresponse(req['id'], error=e.dict(), result=False)
            else:
                self.mq.append(req)
