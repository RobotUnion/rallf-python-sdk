import time
import base64

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rallf.sdk import Task
from rallf.sdk.rallf_error import RallfError
from rallf.tools import SeleniumDeviceFactory
from .image_finder import ImageFinder


class InstallApp(Task):
    """ This Task installs a Google Play App given the icon and the search keywords.
        It scrolls down to find the given icon.
        Tested in Android 7 with resolution 720x1280 (WxH)
    """
    def __init__(self, manifest, robot, input, output):
        super().__init__(manifest, robot, input, output)
        self.device = None
        self.wait = None
        self.wait_for = lambda by, selector: self.wait.until(EC.presence_of_element_located((by, selector)))

        self.kbmap = {
            "special": {
                ' ': {
                    "y": 1226,
                    "x": 400
                },
                '.': {
                    "y": 1226,
                    "x": 573
                },
                "continue": {
                    "y": 1226,
                    "x": 660,
                    "aliases": ["search", "next", "go", "enter"]
                },
                "backspace": {
                    "y": 1126,
                    "x": 660,
                    "aliases": ["delete"]
                },
                "caps": {
                    "y": 1126,
                    "x": 57
                },
                "numbers": {
                    "y": 1226,
                    "x": 57
                },
                "letters": {
                    "y": 1226,
                    "x": 57
                }
            },
            "chars": {
                "1234567890": {
                    "y": 926,
                    "xrange": [40, 680]
                },
                "qwertyuiop": {
                    "y": 926,
                    "xrange": [40, 680]
                },
                "asdfghjkl": {
                    "y": 1026,
                    "xrange": [76, 644]
                },
                "zxcvbnm": {
                    "y": 1126,
                    "xrange": [145, 570]
                }
            }
        }

    def keyboard_write(self, text):
        mode = "lowercase"
        for letter in text:
            if letter.isupper():
                self.device.tap([self.keyboard_coords("caps")])
            if letter.isdigit():
                self.device.tap([self.keyboard_coords("numbers")])
                mode = "numbers"
            self.device.tap([self.keyboard_coords(letter.lower())])
            if mode == "numbers":
                self.device.tap([self.keyboard_coords("letters")])
                mode = "lowercase"

    def keyboard_special(self, special):
        self.device.tap([self.keyboard_coords(special)])

    def keyboard_coords(self, letter):
        special = self.kbmap['special']
        if letter in special.keys():
            return special[letter]['x'], special[letter]['y']

        chars = self.kbmap['chars']
        for key in chars.keys():
            sep = int((chars[key]['xrange'][1] - chars[key]['xrange'][0])/(len(key) - 1))
            if letter in key:
                x = chars[key]['xrange'][0] + key.index(letter) * sep
                return x, chars[key]['y']

    def warmup(self):
        factory = SeleniumDeviceFactory(self.robot)
        self.device = factory.build('android4.4.2')
        self.wait = WebDriverWait(self.device, 10)
        # Go Home
        self.logger.debug("go home")
        self.device.press_keycode(0x3)
        time.sleep(1)
        self.logger.info("WARMUP!!!")
        super().warmup()

    def install(self, input):
        self.logger.debug("install started!")
        icon_file = open("app-logo.png", "wb")
        icon_file.write(base64.b64decode(input['logo']))
        icon_file.flush()
        finder = ImageFinder("app-logo.png")

        # open google play
        self.logger.debug("open google play")
        self.device.tap([(610, 1200)])
        time.sleep(3)

        # tap on search bar
        self.device.tap([(240, 110)])
        time.sleep(1)
        self.keyboard_write(input['search'])
        self.keyboard_special("continue")
        size = self.device.get_window_size()
        self.logger.debug("SIZE: %s" % size)

        scrolls = 0
        while scrolls < 20:
            time.sleep(2)
            self.device.get_screenshot_as_file("screen.png")
            match = finder.match("screen.png")
            self.logger.debug("RES: %s" % match)
            if match['matches'] > 0.99:
                self.logger.debug("APP found!!")
                self.device.tap([match['coords']])
                return
            scrolls += 1
            actions = TouchAction(self.device)
            actions.press(x=int(size['width'] * 0.4), y=int(size['height'] * 0.8))
            actions.wait(1000)
            actions.move_to(x=int(size['width'] * 0.6), y=int(size['height'] * 0.2))
            actions.release()
            actions.perform()

        raise RallfError(32000, "app not found")

    def cooldown(self):
        self.logger.info("cooldown!!!")
        try:
            self.device.close()
        except WebDriverException:
            self.logger.warning("device already closed")
