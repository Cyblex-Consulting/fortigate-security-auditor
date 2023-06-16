import os
import sys
import inspect
from checker import Checker

# Imports all python files as checks

checks = []

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    module_name = "checks." + module[:-3]
    __import__(module_name, locals(), globals())

# Return all checker classes order by name
def classes():
    classes = Checker.__subclasses__()
    return sorted(classes, key=lambda x: str(x))
