def crash_me(s: str) -> None:
    if len(s) > 0 and s[0] == 'b':
        if len(s) > 1 and s[1] == 'a':
            if len(s) > 2 and s[2] == 'd':
                if len(s) > 3 and s[3] == '!':
                    raise Exception()


# test_dyn_import.py
import importlib
from inspect import isfunction

def call_func(full_module_name, func_name, *argv):
    module = importlib.import_module(full_module_name)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isfunction(attribute) and attribute_name == func_name:
            attribute(*argv)

import os


directory = 'sample_programs/mutants/'

from importlib import import_module
from fuzzingbook.ExpectError import ExpectTimeout

def run_program(filename, s):
    try:
        with ExpectTimeout(1):
            call_func('.'.join(directory.split('/')) + filename.strip('.py'), 'crash_me', s)
            return True
    except:
#         print('Syntax Error (%s)' % self.mutant.name)
        return False
#     raise Exception('Unhandled exception during test execution')
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

from fuzzingbook.GreyboxFuzzer import Mutator, Seed, Sequence, PowerSchedule, GreyboxFuzzer, FunctionCoverageRunner, AFLFastSchedule, CountingGreyboxFuzzer 


class AFLFastSchedule(AFLFastSchedule):
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = get_mutation_score(seed.data)

import time

n = 10000
seed_input = "good"
fast_schedule = AFLFastSchedule(5)
fast_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), fast_schedule)
start = time.time()
fast_fuzzer.runs(FunctionCoverageRunner(crash_me), trials=n)
end = time.time()

print(fast_fuzzer.population)