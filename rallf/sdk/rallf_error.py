
class RallfError(RuntimeError):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}
