import os

from rallf.sdk.caller import Caller
from rallf.sdk.listener import Listener
from rallf.sdk.logger import Logger


class Task:

    def __init__(self, manifest, robot, input, output):
        self.manifest = manifest
        self.robot = robot
        self.finished = False
        self.status = "stopped"
        self.logger = Logger(input, output)
        self.caller = Caller(input, output)
        self.listener = Listener(input, output)
        self.home = "%s/data/%s" % (robot.home, manifest['fqtn'])

    def warmup(self):
        self.status = "ready"

    def waitloop(self):
        while not self.finished:
            self.listener.listen(self)

    def main(self, input):
        pass

    def cooldown(self):
        self.status = "finished"

    def finish(self):
        self.status = "terminating"
        self.finished = True
