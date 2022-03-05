import sys
import time

from typing import Tuple, List, Callable, Set, Any
from fuzzingbook.GreyboxFuzzer import Mutator, Seed, Sequence, CountingGreyboxFuzzer, AFLFastSchedule,getPathID
from fuzzingbook.MutationFuzzer import FunctionRunner
from fuzzingbook.Coverage import Coverage
from utils import *

class FunctionMutantsRunner(FunctionRunner):
    def __init__(self, function: Callable, program_num:str = '1') -> None:
        """Initialize.  `function` is a function to be executed"""
        self.function = function
        self.program_num = program_num

    def run_function(self, inp: str) -> Any:
        try:
            result = super().run_function(inp)
        except Exception as exc:
            raise exc

        self._coverage = run_mutants(inp,self.program_num)
        return result

    def coverage(self) -> Set[BugID]:
        return self._coverage
    

class MutationAnalysisSchedule(AFLFastSchedule):
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = 1 / (self.path_frequency[getPathID(seed.coverage)] ** self.exponent)

class Mutation_GreyboxFuzzer(CountingGreyboxFuzzer):
    """Count how often individual paths are exercised."""

    def reset(self):
        """Reset path frequency"""
        super().reset()
        self.schedule.path_frequency = {}

    def run(self, runner: FunctionMutantsRunner) -> Tuple[Any, str]:  # type: ignore
        """Inform scheduler about path frequency"""
        result, outcome = super().run(runner)

        path_id = getPathID(runner.coverage())
        if path_id not in self.schedule.path_frequency:
            self.schedule.path_frequency[path_id] = 1
        else:
            self.schedule.path_frequency[path_id] += 1

        return(result, outcome)

if __name__ == "__main__":
    program_num = '4'
    if len(sys.argv)>1:
        program_num = str(sys.argv[1])

    n = 10000
    mutant_analysis_schedule = MutationAnalysisSchedule(5)
    mutant_fuzzer = Mutation_GreyboxFuzzer(programs[program_num]['seeds'], Mutator(), mutant_analysis_schedule)
    start = time.time()
    mutant_fuzzer.runs(FunctionMutantsRunner(programs[program_num]['function'], program_num), trials=n)
    end = time.time()

    print(mutant_fuzzer.population)