import uuid


class Execution:
    def __init__(self, task, func, robot, input):
        self.id = uuid.uuid4()
        self.task = task
        self.func = func
        self.robot = robot
        self.input = input

