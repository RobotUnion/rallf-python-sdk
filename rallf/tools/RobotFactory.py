from rallf.tools import Robot
import json, pathlib

class RobotFactory:
    def __init__(self):
        pass

    def createFromDir(self, dir):
        if not pathlib.Path(dir).is_dir():
            raise NotADirectoryError("%s is not a valid directory" % dir)
        bot = Robot

        # Robot devices
        bot.devices = json.load(open(dir + "/devices.json", "r"))

        # Robot skills
        bot.skills = json.load(open(dir + "/skills.json", "r"))

        # Robot's knowledge base
        bot.kb = json.load(open(dir + "/kb.json", "r"))

        return bot

    def createEmpty(self):
        return Robot()
