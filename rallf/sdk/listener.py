import time
from json.decoder import JSONDecodeError

from rallf.sdk.rallf_error import RallfError
from rallf.tools.communicator import Communicator


class Listener(Communicator):
    def __init__(self, input, output):
        super().__init__(input, output)

    def listen(self, task):
        try:
            req = self.wait()
            try:
                if 'method' in req:
                    if req['method'] != "delegate":
                        raise RallfError(-32601, "Invalid method '%s'" % req['method'])
                    try:
                        task.network.event("routine:start", {"name": req['params']['routine'], "id": req["id"]})

                        if req['params']['routine'] not in task.manifest['exports']:
                            raise RallfError(-32601, "Method '%s' not exported in Task %s" % (req['params']['routine'], task.manifest['fqtn']))

                        resp = getattr(task, req['params']['routine'])(req['params']['args'])
                        task.network.rpcresponse(id=req['id'], result=resp, error=False)
                    except RallfError as e:
                        task.network.rpcresponse(id=req['id'], error=e.dict(), result=False)
                    finally:
                        task.network.event("routine:end", {"name": req['params']['routine'], "id": req["id"]})
                else:
                    self.mq.append(req)

            except RallfError as e:
                task.network.rpcresponse(id=req['id'], error=e.dict(), result=False)

        except JSONDecodeError:
            task.network.rpcresponse(id=None, error={"code": -32700, "message": "Parse error"})
        except (EOFError, InterruptedError):
            task.finish()
