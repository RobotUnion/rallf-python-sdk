#!/usr/bin/env python3
import json
import signal
import sys
import argparse

from rallf.args import RallfArgs
from rallf.tools.execution import Execution
from rallf.tools.robot_factory import RobotFactory
from rallf.tools.runner import Runner
from rallf.tools.task_factory import TaskFactory


def sigint_handler(sig, frame):
    raise InterruptedError()


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    p = argparse.ArgumentParser(description="Rallf developer tool", prog="Rallf-SDK")
    p.add_argument("command", nargs=1, action="store", choices=["new-task", "run", "event"], help="rallf command")
    p.add_argument("task_dir", action="store", nargs="?", default=".", help="task directory (default: current)")
    p.add_argument("-f", "--func", dest="func", default=None, action="store", help="the routine to execute (default: None)")
    p.add_argument("-r", "--robot", dest="robot", action="store", default=None, help="robot to invoke (default: nullbot)")
    p.add_argument("-m", "--mocks", dest="mocks", action="store", default=None, help="mocks directory (default: None)")
    p.add_argument("-i", "--input", dest="input", default="{}", action="store", help="task's input in JSON (default: {})")
    p.add_argument("-v", "--version", action="version", version="%(prog)s 0.2.3", help="prints the SDK version")

    args = RallfArgs()
    p.parse_args(namespace=args)

    cmd_line = args.getProcessed()

    rf = RobotFactory()

    bot = rf.createEmpty() if cmd_line.robot is None else rf.createFromDir(cmd_line.robot)

    tf = TaskFactory()
    task = tf.createFromDir(cmd_line.task_dir, bot, sys.stdin, sys.stdout)

    if cmd_line.func is not None and cmd_line.func not in task.manifest['exports']:
        raise RuntimeError("%s function not exported in package" % cmd_line.func)

    x = Execution(task, cmd_line.func, bot, json.loads(cmd_line.input))

    Runner.execute(x)


if __name__ == "__main__":
    main()
