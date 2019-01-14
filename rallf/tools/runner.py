from pathlib import Path

from rallf.tools.execution import Execution
import os


class Runner:
    def __init__(self):
        pass

    @staticmethod
    def execute(execution: Execution):
        home = Path(execution.task.home).absolute()

        if not home.exists(): home.mkdir(parents=True, exist_ok=True)
        os.chdir(str(home))
        execution.task.warmup()
        execution.task.network.event("warmup:end")
        if execution.func is None: execution.task.waitloop()
        else: print(getattr(execution.task, execution.func)(execution.input))
        execution.task.cooldown()
