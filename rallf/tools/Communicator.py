import json


class Communicator:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def rpccall(self, method, params, id):
        json.dump({"jsonrpc": "2.0", "method": method, "params": params, "id": id}, self.output)
        return self.listenfor(id)

    def call(self, type, routine, args):
        return self.rpccall(type, {"routine": routine, "params": args}, id=0)

    def log(self, msg, level=0, data=None):
        return self.rpccall("log", {"message": msg, "level": level, "data": data}, id=0)

    def listen(self):
        return json.dumps(self.input.readline())

    def listenfor(self, id):
        input = self.listen()
        assert input['id'] == id
        return input
