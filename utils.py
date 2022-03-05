import os
import importlib

from importlib import import_module
from typing import Tuple
from fuzzingbook.ExpectError import ExpectTimeout
from inspect import isfunction
from sample_programs.crash_me.crash_me import crash_me
from sample_programs.balanced_parantheses.balanced_parantheses import balanced_parantheses
from sample_programs.evaluate_expression.evaluate_expression import evaluate_expression


programs = {
    '1': { 'name': 'crash_me', 'function': crash_me,
        'seeds':['good']
    },
    '2': { 'name': 'balanced_parantheses', 'function': balanced_parantheses,
        'seeds':['({good[]})', '{[()()[]{()}}', '{[[[))}]{]']
    },
    '3': { 'name': 'evaluate_expression', 'function': evaluate_expression,
        'seeds':['2*(5+5*2)/3+(6/2+8)', '1*2+3', '1-5']
    },
}
BugID = Tuple[int,str]
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
            call_func('.'.join(directory(program_num).split('/')) + filename.strip('.py'), programs[program_num]['name'], s)
            return 
    except Exception as e:
        return e.__class__.__name__
    raise Exception('Exception not caught!!')

def run_mutants(data, program_num = '1'):
    total = len(os.listdir(directory(program_num)))
    _coverage = set()
    for i,filename in enumerate(os.listdir(directory(program_num))):
        f = os.path.join(directory(program_num), filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(os.path.join(directory(program_num) +filename)) as handler:
                exc = run_program_killed(filename, program_num ,data)
                if exc: _coverage.add((i,exc))
                
    return _coverage
