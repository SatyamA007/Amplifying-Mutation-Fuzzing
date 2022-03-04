import os
import importlib

from importlib import import_module
from fuzzingbook.ExpectError import ExpectTimeout
from inspect import isfunction
from sample_programs.crash_me.crash_me import crash_me


programs = {
    '1': { 'name': 'crash_me', 'function': crash_me,
        'seeds':['good']
    },
    '2': { 'name': 'crash_me', 'function': crash_me,
        'seeds':['good']
    },
}

mute = True

def directory(program_num:str):
    return 'sample_programs/'+programs[program_num]['name']+'/mutants/'

def call_func(full_module_name, func_name, *argv):
    module = importlib.import_module(full_module_name)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isfunction(attribute) and attribute_name == func_name:
            attribute(*argv)

def run_program_killed(filename, program_num, s):
    try:
        with ExpectTimeout(1, mute = mute):
            #print('.'.join(directory(program_num).split('/')) + filename.strip('.py'), programs[program_num]['name'], s)
            call_func('.'.join(directory(program_num).split('/')) + filename.strip('.py'), programs[program_num]['name'], s)
            return False
    except:
        return True
    return True

def run_mutants(data, program_num = '1'):
    total = len(os.listdir(directory(program_num)))
    _coverage = set()
    for i,filename in enumerate(os.listdir(directory(program_num))):
        f = os.path.join(directory(program_num), filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(os.path.join(directory(program_num) +filename)) as handler:
                if run_program_killed(filename, program_num ,data):
                    _coverage.add(i)

    return _coverage
