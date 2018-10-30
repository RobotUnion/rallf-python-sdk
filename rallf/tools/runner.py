from rallf.tools.execution import Execution
import os


class Runner:
    def __init__(self):
        pass

    def execute(self, execution: Execution):
        DIR = "/tmp/%s" % execution.id
        os.mkdir(DIR); os.chdir(DIR)
        # os.chroot(DIR)
        getattr(execution.task, 'warmup')()
        if execution.func is None: getattr(execution.task, "waitloop")()
        else: getattr(execution.task, execution.func)(execution.input)
        getattr(execution.task, 'cooldown')()

        #os.unlink(DIR)
