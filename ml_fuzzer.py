import time

from typing import Dict, Tuple, List, Callable, Set, Any
from fuzzingbook.GreyboxFuzzer import Mutator, Seed, Sequence, CountingGreyboxFuzzer, AFLFastSchedule,getPathID
from fuzzingbook.MutationFuzzer import FunctionRunner
from fuzzingbook.Fuzzer import Runner
from fuzzingbook.Coverage import Coverage
from utils import *
from sample_programs.crash_me import crash_me

class Seed_with_mutants(Seed):
     def __init__(self, data: str) -> None:
        """Initialize from seed data"""
        self.data = data
        self.coverage: Set[int] = set()
        self.mutants: Set[int] = set()
        self.energy = 0.0

class FunctionMLRunner(FunctionRunner):
    def run_function(self, inp: str) -> Any:
        with Coverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        try:
            result = super().run_function(inp)
        except Exception as exc:
            raise exc
        
        self._coverage = cov.coverage()
        self._mutantsCovered = run_mutants(inp)
        return result

    def coverage(self):
        return self._coverage, self._mutantsCovered
    

class MLSchedule(AFLFastSchedule):
    def __init__(self, exponent_x1: float, exponent_x2: float) -> None:
        """Constructor"""
        self.path_frequency: Dict = {}
        self.mutant_frequency: Dict = {}
        self.exponent_x1 = exponent_x1
        self.exponent_x2 = exponent_x2

    def assignEnergy(self, population: Sequence[Seed_with_mutants]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = 1 / (self.path_frequency[getPathID(seed.coverage)] ** self.exponent_x1)
            seed.energy *= 1 / (self.mutant_frequency[getPathID(seed.mutants)] ** self.exponent_x2)
    
class ML_GreyboxFuzzer(CountingGreyboxFuzzer):
    """Count how often individual paths are exercised."""

    def reset(self):
        """Reset path frequency"""
        super().reset()
        self.schedule.path_frequency = {}
        self.schedule.mutant_frequency = {}
        self.mutants_seen = set()

    def run(self, runner: FunctionMLRunner) -> Tuple[Any, str]:  # type: ignore
        """Inform scheduler about path frequency"""
        result, outcome = self.super_run(runner)

        path_id_1 = getPathID(runner.coverage()[0])
        path_id_2 = getPathID(runner.coverage()[1])
        if path_id_1 not in self.schedule.path_frequency:
            self.schedule.path_frequency[path_id_1] = 1
        else:
            self.schedule.path_frequency[path_id_1] += 1
        
        if path_id_2 not in self.schedule.mutant_frequency:
            self.schedule.mutant_frequency[path_id_2] = 1
        else:
            self.schedule.mutant_frequency[path_id_2] += 1

        return(result, outcome)

    def super_run(self, runner: FunctionMLRunner) -> Tuple[Any, str]: 
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = runner.run(self.fuzz())

        new_coverage = frozenset(runner.coverage()[0])
        new_mutants = frozenset(runner.coverage()[1])
        
        if new_coverage not in self.coverages_seen or new_mutants not in self.mutants_seen:
            # We have new coverage
            seed = Seed_with_mutants(self.inp)
            seed.coverage = runner.coverage()[0]
            seed.mutants = runner.coverage()[1]
            self.coverages_seen.add(new_coverage)
            self.mutants_seen.add(new_mutants)
            self.population.append(seed)
        return (result, outcome)



if __name__ == "__main__":
    n = 10000
    seed_input = "good"
    ml_schedule = MLSchedule(5,5)
    ml_fuzzer = ML_GreyboxFuzzer([seed_input], Mutator(), ml_schedule)
    start = time.time()
    ml_fuzzer.runs(FunctionMLRunner(crash_me), trials=n)
    end = time.time()

    print(ml_fuzzer.population)