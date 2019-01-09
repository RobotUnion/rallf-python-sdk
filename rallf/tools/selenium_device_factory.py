import os

from selenium.webdriver import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from appium import webdriver as appium_webdriver

from rallf.sdk.rallf_error import RallfError


class SeleniumDeviceFactory:
    def __init__(self, robot):
        self.robot = robot

    def build(self, key, profile_dir=None):
        definition = self.robot.devices[key]
        if 'bin' in definition and not os.path.isabs(definition['bin']):
            definition['bin'] = os.path.abspath("%s/bin/%s" % (self.robot.home, definition['bin']))
        if 'driver' in definition and not os.path.isabs(definition['driver']):
            definition['driver'] = os.path.abspath("%s/bin/%s" % (self.robot.home, definition['driver']))

        if definition['platform'] == 'selenium':

            if definition['kind'] == 'driver':
                if definition['device'] == 'firefox':
                    binary = FirefoxBinary(definition['bin'])
                    profile = FirefoxProfile(profile_dir)
                    return FirefoxDriver(profile, binary)
                if definition['device'] == 'chrome':
                    service = Service(definition['driver'])
                    service.start()
                    capabilities = {'chrome.binary': definition['bin']}
                    return webdriver.Remote(service.service_url, capabilities)
                raise RallfError(-32001, "Selenium browser not supported, please use another factory")

            if definition['kind'] == 'remote':
                if definition['device'] == 'android':
                    capabilities = {
                        'automationName': 'uiautomator2',
                        'platformName': 'Android',
                        'deviceName': "test",
                        "appPackage": definition['app_package'],
                        "appActivity": definition['app_activity']
                    }
                    return appium_webdriver.Remote(command_executor="%s/wd/hub" % definition['server'], desired_capabilities=capabilities)

            raise RallfError(-32002, "Selenium kind not supported, please use another factory")
        raise RallfError(-32003, "Non-selenium devices are not supported, please use another factory")
