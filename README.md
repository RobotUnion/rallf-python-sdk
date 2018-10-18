# RALF Python SDK
RALLF SDK provides the tools to create tasks for rallf robots (rallf.com) using python3.

## Installation
### Using Python Package Index (PyPI)
```bash
pip3 install rallf
```

### From source
```bash
git clone https://github.com/RobotUnion/rallf-python-sdk
cd rallf-python-sdk
python3 setup.py install
```

## Basic usage (hello bot)
### Create `hello.py`
```python3
# File: hello.py

import rallf

'''
  Hello task opens github and returns the title of the page upon it is loaded.
  To learn more about python selenium api, see https://selenium-python.readthedocs.io/
'''
class Hello(rallf.Task):

    # implementing self.run is required for tasks
    def run(self, input):
        # Log stuff via the available logger
        self.logger.debug('Hello Bot')
    
        # get a firefox instance
        browser = self.robot.devices['firefox']
        browser.get('https://github.com')
        return browser.getTitle()
    
```
### Try it
```bash
rallf start hello
```

## Extended usage
### Injected objects
- robot
- input
### Inter-task communication (task delegates)
