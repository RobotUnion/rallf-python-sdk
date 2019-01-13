from json.decoder import JSONDecodeError

from rallf.sdk.rallf_error import RallfError
from rallf.tools.communicator import Communicator


class Listener(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def listen(self, task):
        try:
            req = self.wait()
            if 'method' in req:
                try:
                    resp = getattr(task, req['params']['routine'])(req['params']['args'])
                    task.network.rpcresponse(id=req['id'], result=resp, error=False)
                except RallfError as e:
                    task.network.rpcresponse(id=req['id'], error=e.dict(), result=False)
            else:
                self.mq.append(req)

        except JSONDecodeError:
            task.network.rpcresponse(id=None, error={"code": -32700, "message": "Parse error"})
        except (EOFError, InterruptedError):
            task.finish()
