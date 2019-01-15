import time
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

        execution.task.network.event("routine:start", {"name": "warmup"})
        execution.task.warmup()
        execution.task.network.event("routine:end", {"name": "warmup"})
        if execution.func is None: execution.task.waitloop()
        else:
            execution.task.network.event("routine:start", {"name": execution.func})
            print(getattr(execution.task, execution.func)(execution.input))
            execution.task.network.event("routine:end", {"name": execution.func})
        execution.task.network.event("routine:start", {"name": 'cooldown'})
        execution.task.cooldown()
        execution.task.network.event("routine:end", {"name": 'cooldown'})
