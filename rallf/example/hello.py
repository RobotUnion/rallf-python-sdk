from rallf.sdk.task import Task


class Hello(Task):
    def __init__(self, robot, input, output):
        super().__init__(robot, input, output)

    def main(self, input):
        self.logger.debug("Hello task!", input)

    def warmup(self):
        self.logger.debug("WARMUP!!!")

    def cooldown(self):
        self.logger.debug("cooldown!!!")
