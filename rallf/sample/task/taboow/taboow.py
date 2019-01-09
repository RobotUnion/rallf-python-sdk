import os
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rallf.sdk import Task
from rallf.tools import SeleniumDeviceFactory


class Taboow(Task):
    def __init__(self, manifest, robot, input, output):
        super().__init__(manifest, robot, input, output)
        self.browser = None
        self.ffoxProfile = "%s/firefox_profile" % self.home
        self.wait = None
        self.wait_for = lambda by, selector: self.wait.until(EC.presence_of_element_located((by, selector)))

    def warmup(self):
        self.logger.info("WARMUP!!!")
        if not os.path.exists(self.ffoxProfile): os.mkdir(self.ffoxProfile)
        factory = SeleniumDeviceFactory(self.robot)
        self.browser = factory.build('firefox63', self.ffoxProfile)
        self.wait = WebDriverWait(self.browser, 10)

    def dashboard(self, input):
        self.logger.debug("dashboard started!")
        self.logger.debug(len(self.robot.devices))
        assert self.browser is not None
        self.browser.get("https://taboow.org/panel/dashboard")
        continue_browsing = self.wait_for(By.XPATH, "/html/body/div[2]/div[4]/div/div/div[3]/button[2]")
        continue_browsing.click()
        time.sleep(10)

    def cooldown(self):
        self.logger.info("cooldown!!!")
        try:
            profile_tmp_path = self.browser.capabilities['moz:profile']
            os.system("cp -r %s/* %s" % (profile_tmp_path, self.ffoxProfile))
            self.browser.close()
        except WebDriverException:
            self.logger.warning("driver already closed")
