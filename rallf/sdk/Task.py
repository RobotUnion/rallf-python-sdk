import threading
import time


class Task(threading.Thread):
  def __init__(self, robot, input):
    super().__init__()
    self.manifest = None
    self.robot = robot
    self.input = input
    self.finished = False
    self.status = "stopped"

  def warmup(self):
    self.status = "ready"

  def run(self):
    self.warmup()
    while not self.finished: time.sleep(1)
    self.cooldown()

  def main(self, input):
    pass

  def delegate(self, fqtn, data):
    pass

  def cooldown(self):
    self.status = "finished"

  def mock(self, input):
    return "this is a test"

  def finish(self):
    self.status = "terminating"
    self.finished = True