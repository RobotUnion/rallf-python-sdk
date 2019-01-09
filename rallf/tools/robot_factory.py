import json
import pathlib

from rallf.sdk.robot import Robot


class RobotFactory:

    @staticmethod
    def createFromDir(dir):
        if not pathlib.Path(dir).is_dir():
            raise NotADirectoryError("%s is not a valid directory" % dir)
        return Robot(dir, json.load(open(dir + "/skills.json", "r")), json.load(open(dir + "/devices.json", "r")))

    def createEmpty(self):
        return Robot("/tmp/empty", {}, {})
