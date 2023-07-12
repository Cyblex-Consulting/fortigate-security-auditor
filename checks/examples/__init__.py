import os
import sys
import inspect
from checker import Checker

# Imports all python files as checks

parent_folder = os.path.dirname(__file__)
for module in os.listdir(parent_folder):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(f'checks.{os.path.basename(parent_folder)}.{module[:-3]}', locals(), globals())

# Return all checker classes
def classes():
    classes = Checker.__subclasses__()
    return classes