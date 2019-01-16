import time

from selenium.common.exceptions import WebDriverException

from rallf.sdk import Task
from rallf.tools import SeleniumDeviceFactory


class Title(Task):
    def __init__(self, manifest, robot, input, output):
        super().__init__(manifest, robot, input, output)
        self.browser = None

    def warmup(self):
        self.logger.info("Warming-up the engine!")
        factory = SeleniumDeviceFactory(self.robot)
        self.browser = factory.build('firefox')

    def run(self, input=None):
        assert self.browser is not None
        self.browser.get(input['url'])
        time.sleep(10)
        return self.browser.title

    def cooldown(self):
        self.logger.info("cooldown!!!")
        try:
            self.browser.close()
        except WebDriverException:
            self.logger.warning("driver already closed")

        super().cooldown()
