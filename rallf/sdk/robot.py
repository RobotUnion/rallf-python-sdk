from rallf.sdk.caller import Caller


class Robot:
    def __init__(self):
        self.devices = []
        self.skills = []
        self.home = {}
        self.caller = Caller

    def use(self, skill, data):
        return self.caller.use(skill, data)
