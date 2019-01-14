# RALF Python SDK


[![Website](https://img.shields.io/website-up-down-green-red/https/api.rallf.com.svg?label=api)](https://rallf.com)
[![GitHub license](https://img.shields.io/github/license/robotunion/rallf-python-sdk.svg)](https://github.com/RobotUnion/rallf-python-sdk/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/robotunion/rallf-python-sdk.svg)](https://github.com/robotunion/rallf-python-sdk/issues)
[![PyPI](https://img.shields.io/pypi/v/rallf.svg)](https://pypi.org/pypi/rallf/)
[![Python Versions](https://img.shields.io/pypi/pyversions/rallf.svg)](https://pypi.org/pypi/rallf/)
[![Requirements Status](https://requires.io/github/RobotUnion/rallf-python-sdk/requirements.svg?branch=master)](https://requires.io/github/RobotUnion/rallf-python-sdk/requirements/?branch=master)


RALLF SDK provides the tools to create tasks for rallf robots (rallf.com) using python3.

**Disclaimer! This package is in development stage (unstable), it may be potentially buggy**

## Installation
### Using Python Package Index (PyPI)
```bash
pip3 install rallf
```

### From source
```bash
git clone https://github.com/RobotUnion/rallf-python-sdk
cd rallf-python-sdk
pip3 install -r requirements.txt
python3 setup.py install
```

## Getting started (hello bot-task)
In order to get started with robot task development, just run `python3 -m rallf.cli create-project "hello"` and it will create a basic project with the files explained below.
### `hello.py`
```python3
# File: hello.py

from rallf import Task

'''
  Hello task opens github and returns the title of the page upon it is loaded.
  To learn more about python selenium api, see https://selenium-python.readthedocs.io/
'''
class Hello(Task):

    # implementing self.run is required for tasks, not for skills
    def run(self, input):
        # Log stuff via the available logger
        self.logger.debug('Hello Bot')
    
        # get a firefox instance
        browser = self.robot.devices['firefox']
        browser.get('https://github.com')
        return browser.getTitle()
    
```
### Try it (rallf cli)
To use the `cli` you can use either the binary included in the package

`rallf <args>`

or executing directly from python

`python3 -m rallf.cli <args>`

#### Run `run` method using the `CLI`
```bash
rallf run . -f run
```

#### Run `run` method using the `jsonrpc` api
```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "delegate_local", "params": {"routine": "run", "args": {}}}' | rallf run .
```

#### Get help 
```bash
rallf -h
```

## Extended usage

### Task Manifest
Task manifest is mandatory for rallf.com tasks, but not necessary for developing, visit [manifest reference](undefined) to learn more in-deep about task manifests.
```js
/* File manifest.json */
{
  "title": "Hello Task",
  "description": "This tasks logs hello and returns the <title> of github.com",
  "long-description": "@README.md",
  "fqtn": "com.example.hello",
  "type": "task", /* choices: task, skill */
  "main": "hello.Hello",
  "exports": ["run"], /* default: ["run"] */
  "devices": ["firefox"],
  "skills": [],
  "permissions": {
    "uris": ["https://github.com", "https://google.com"],
    "devices": ["firefox", "chrome"],
    "skills": {
      "com.example.facebook": ["likePage", "likePost"],
      "com.example.gmail": ["search", "likePost"]
    },
  }
}
```

### Injected objects
- `self.robot` this object is injected in the task creation
- `input` this parameter is passed to the `run(self, input)` function

### Inter Task Communication (ITC)
- Call other tasks from the market ([rallf.com](https://rallf.com))
- Use robot skills

### Task lifecycle callbacks
- `warmup(self)` this **optional** method is executed some time before the task starts to speed-up the rest of calls.
- `run(self, input)` this **required** method handles the work of the task and is triggered at start of the task.
- `cooldown(self)` this **optional** method is called when the task is going to be some time without use.

### Task vs Skill
A common question is the difference between Task and Skill inside the RALLF ecosystem, the main difference is that
Tasks only have one method called `run` and the skill can have many, so technically a Task is a subtype of Skill,
and also a Skill can implement the `run` method and can be used as Task too.