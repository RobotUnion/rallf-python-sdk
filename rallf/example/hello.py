from rallf.sdk import Task


class Hello(Task):
    def __init__(self, robot, caller, logger):
        super().__init__(robot, caller, logger)

    def main(self, input):
        self.logger.debug("Hello task!")

    def warmup(self):
        self.logger.debug("WARMUP!!!")

    def cooldown(self):
        self.logger.debug("cooldown!!!")