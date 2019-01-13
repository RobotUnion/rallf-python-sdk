import json
import os


class TaskFactory:

    @staticmethod
    def createFromDir(dir, robot, input, output):
        manifest_path = "%s/config/manifest.json" % dir

        if not os.path.isfile(manifest_path):
            raise FileNotFoundError("manifest.json not found in package")

        manifest = json.load(open(manifest_path, "r"))
        task_class = manifest['main'].split(".")
        package = ".".join(task_class[:-1])
        classname = task_class[-1]
        Task = getattr(__import__(package, fromlist=[classname]), classname)
        return Task(manifest, robot, input, output)
