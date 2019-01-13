from rallf.tools.execution import Execution
import os


class Runner:
    def __init__(self):
        pass

    def execute(self, execution: Execution):
        DIR = execution.task.home

        if not os.path.exists(DIR): os.mkdir(DIR)
        os.chdir(DIR)
        # os.chroot(DIR)
        execution.task.warmup()
        execution.task.network.event("warmup:end")
        if execution.func is None: execution.task.waitloop()
        else: getattr(execution.task, execution.func)(execution.input)
        execution.task.cooldown()

        #os.unlink(DIR)

