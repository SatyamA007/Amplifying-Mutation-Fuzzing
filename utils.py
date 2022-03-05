import os
import importlib

from importlib import import_module
from typing import Tuple
from fuzzingbook.ExpectError import ExpectTimeout
from inspect import isfunction
from pyrsistent import mutant
from sample_programs.crash_me.crash_me import crash_me
from sample_programs.balanced_parantheses.balanced_parantheses import balanced_parantheses
from sample_programs.evaluate_expression.evaluate_expression import evaluate_expression


programs = {
    '1': { 'name': 'crash_me', 'function': crash_me,
        'seeds':['good'], 'codeLines': 6
    },
    '2': { 'name': 'balanced_parantheses', 'function': balanced_parantheses,
        'seeds':['({good[]})', '{[()()[]{()}}', '{[[[))}]{]'], 'codeLines': 22
    },
    '3': { 'name': 'evaluate_expression', 'function': evaluate_expression,
        'seeds':['2*(5+5*2)/3+(6/2+8)', '1*2+3', '1-5'], 'codeLines': 50
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
        with ExpectTimeout(0.01, mute = mute):
            call_func('.'.join(directory(program_num).split('/')) + filename.strip('.py'), programs[program_num]['name'], s)
            return 
    except Exception as e:
        return e.__class__.__name__
    raise Exception('Exception not caught! Please change line 245 of fuzzingbook.ExpectError to return False')

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


def coverageScore(fuzzer, program_num):
    linesCovered = set()
    for paths in fuzzer.coverages_seen:
        if paths:
            for i in paths:
                if i[0] not in ['run_function', 'trace', 'coverage']:
                    linesCovered.add(i[1])
    return len(linesCovered) / programs[program_num]['codeLines'], linesCovered
    
def mutationScore(fuzzer, program_num):
    files = [file for file in os.listdir(directory(program_num)) 
         if os.path.isfile(os.path.join(directory(program_num), file))]
    total = len(files)

    mutantsCovered = set()
    for paths in fuzzer.mutants_seen:
        if paths:
            for i in paths:
                i = list(i)
                mutantsCovered.add(i[0])
    return len(mutantsCovered) / total, mutantsCovered

def score(coverageScore, mutationScore):
    return (1 - coverageScore + 1 - mutationScore)/2