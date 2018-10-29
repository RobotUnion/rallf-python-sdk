import threading
import time

from rallf.sdk import Caller, Logger


class Task(threading.Thread):

  def __init__(self, robot, caller=Caller, logger=Logger):
    super().__init__()
    self.manifest = None
    self.robot = robot
    self.finished = False
    self.status = "stopped"
    self.logger = logger
    self.caller = caller

  def warmup(self):
    self.status = "ready"

  def run(self):
    self.warmup()
    while not self.finished: time.sleep(1)
    self.cooldown()

  def main(self, input):
    pass

  def cooldown(self):
    self.status = "finished"

  def mock(self, input):
    return "this is a test"

  def finish(self):
    self.status = "terminating"
    self.finished = True