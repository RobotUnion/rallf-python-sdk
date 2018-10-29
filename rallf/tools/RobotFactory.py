from rallf.sdk import Robot
import json, pathlib


class RobotFactory:

    @staticmethod
    def createFromDir(dir):
        if not pathlib.Path(dir).is_dir():
            raise NotADirectoryError("%s is not a valid directory" % dir)
        bot = Robot()

        # Robot devices
        bot.devices = json.load(open(dir + "/devices.json", "r"))

        # Robot skills
        bot.skills = json.load(open(dir + "/skills.json", "r"))

        return bot

    def createEmpty(self):
        return Robot()
