from rallf.tools import Execution
import os


class Runner:
    def __init__(self):
        pass

    def execute(self, execution: Execution):
        DIR = "/tmp/%s" % execution.id
        os.mkdir(DIR); os.chdir(DIR)
        # os.chroot(DIR)
        getattr(execution.task, 'warmup')()
        getattr(execution.task, execution.func)(execution.input)
        getattr(execution.task, 'cooldown')()

        #os.unlink(DIR)

