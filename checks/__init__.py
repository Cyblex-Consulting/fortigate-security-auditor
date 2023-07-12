import os
import sys
import inspect
from checker import Checker

# Imports all python files as checks

checks = []

parent_folder = os.path.dirname(__file__)
for folder_name in os.listdir(parent_folder):
    item = f'{parent_folder}/{folder_name}'
    if os.path.isdir(item) and folder_name[:2] != '__':
        __import__(f'checks.{folder_name}', locals(), globals())

# Return all checker classes order by name
def classes():
    classes = Checker.__subclasses__()
    return classes