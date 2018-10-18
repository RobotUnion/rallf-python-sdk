
class Task:
  def __init__(self, robot):
    self.robot = robot

  def warmup(self):
    pass

  def run(self, input):
    pass

  def cooldown(self):
    pass

  def mock(self, input):
    return "this is a test"
