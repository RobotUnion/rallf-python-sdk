from rallf.sdk import Task


class Hello(Task):
    def __init__(self, robot):
        super().__init__(robot)

    def main(self, input):
        self.logger.debug("Hello task!")
