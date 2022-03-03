import os
import importlib

from importlib import import_module
from fuzzingbook.ExpectError import ExpectTimeout
from inspect import isfunction


directory = 'sample_programs/mutants/'


def call_func(full_module_name, func_name, *argv):
    module = importlib.import_module(full_module_name)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isfunction(attribute) and attribute_name == func_name:
            attribute(*argv)

def run_program(filename, s):
    try:
        with ExpectTimeout(1):
            call_func('.'.join(directory.split('/')) + filename.strip('.py'), 'crash_me', s)
            return True
    except:
        return False
    return False

def get_mutation_score(data):
    total = len(os.listdir(directory))
    un_detected = 0
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(os.path.join(directory +filename)) as handler:
                un_detected += run_program(filename, data)

    score = (total - un_detected) / total
#     print(score, un_detected, total)
    return score
