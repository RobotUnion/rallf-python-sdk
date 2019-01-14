from rallf.tools.execution import Execution
import os


class Runner:
    def __init__(self):
        pass

    @staticmethod
    def execute(execution: Execution):
        home = execution.task.home

        if not os.path.exists(home): os.mkdir(home)
        os.chdir(home)
        execution.task.warmup()
        execution.task.network.event("warmup:end")
        if execution.func is None: execution.task.waitloop()
        else: print(getattr(execution.task, execution.func)(execution.input))
        execution.task.cooldown()
