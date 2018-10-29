from rallf.tools import Robot
from .RallfFactory import RallfFactory
import json, pathlib


class RobotFactory(RallfFactory):

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

        return bot

    def createEmpty(self):
        return Robot()
