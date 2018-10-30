import json


class Communicator:
    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.mq = []

    def rpcsend(self, request):
        request.update({"jsonrpc": "2.0"})
        self.output.write("%s\n" % json.dumps(request))

    def rpcreceive(self):
        return json.loads(self.input.readline())

    def rpccall(self, method, params, id=False):
        request = {"jsonrpc": "2.0", "method": method, "params": params}
        if id != False:
            self.rpcsend({**request, **{"id": id}})
            return self.waitfor(id)
        self.rpcsend(request)

    def rpcresponse(self, id=None, result=False, error=False):
        if result is False and error is False or result is not False and error is not False:
            raise RuntimeError("Incompatible response: 'result' and 'error' cannot be the same")

        response = {"jsonrpc": "2.0", "id": id}
        if result is not False: response.update({"result": result})
        elif error is not False: response.update({"error": error})

        self.rpcsend(response)

    def wait(self, forcereceive=False):
        if not forcereceive and len(self.mq) > 0: return self.mq.pop(0)
        return self.rpcreceive()

    def waitfor(self, id):
        while True:
            for i in range(len(self.mq)):
                if "method" not in self.mq[i] and self.mq[i]['id'] == id:
                    return self.mq.pop(i)
            input = self.wait(True)
            if "method" not in input and input['id'] == id: return input
            else: self.mq.append(input)
