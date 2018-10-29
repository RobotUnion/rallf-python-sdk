import json
import os

from .RallfFactory import RallfFactory


class TaskFactory(RallfFactory):

    def createEmpty(self):
        raise NotImplementedError("cannot create empty task")

    def createFromDir(self, dir):
        manifest_path = "%s/manifest.json" % dir

        if not os.path.isfile(manifest_path):
            raise FileNotFoundError("manifest.json not found in package")

        manifest = json.load(open(manifest_path, "r"))
        task_class = manifest['main'].split(".")
        package = ".".join(task_class[:-1])
        classname = task_class[-1]
        Task = getattr(__import__(package, fromlist=[classname]), classname)
        t = Task()
        t.manifest = manifest
        return t
