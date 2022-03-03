import time

from typing import Tuple, List, Callable, Set, Any
from fuzzingbook.GreyboxFuzzer import Mutator, Seed, Sequence, FunctionRunner, AdvancedMutationFuzzer, AFLFastSchedule 
from fuzzingbook.MutationFuzzer import FunctionRunner
from fuzzingbook.Coverage import Coverage, FunctionRunner
from utils import *
from sample_programs.crash_me import crash_me

Location = Tuple[str, int]

class FunctionMutantsRunner(FunctionRunner):
    def run_function(self, inp: str) -> Any:
        with Coverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return result

    def kill_coverage(self) -> Set[Location]:
        return self._coverage

class MutationAnalysisSchedule(AFLFastSchedule):
    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = get_mutation_score(seed.data)

class Mutation_GreyboxFuzzer(AdvancedMutationFuzzer):
    """MutationAnalysis-guided mutational fuzzing."""

    def reset(self):
        """Reset the initial population, seed index, coverage information"""
        super().reset()
        self.mutants_killed = set()
        self.population = []  # population is filled during greybox fuzzing

    def run(self, runner: FunctionMutantsRunner) -> Tuple[Any, str]:  # type: ignore
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_kill_coverage = frozenset(runner.kill_coverage())
        if new_kill_coverage not in self.mutants_killed:
            # We have new coverage
            seed = Seed(self.inp)
            seed.coverage = runner.kill_coverage()
            self.mutants_killed.add(new_kill_coverage)
            self.population.append(seed)

        return (result, outcome)

if __name__ == "__main__":
    n = 10000
    seed_input = "good"
    mutant_analysis_schedule = MutationAnalysisSchedule(5)
    mutant_fuzzer = Mutation_GreyboxFuzzer([seed_input], Mutator(), mutant_analysis_schedule)
    start = time.time()
    mutant_fuzzer.runs(FunctionMutantsRunner(crash_me), trials=n)
    end = time.time()

    print(mutant_fuzzer.population)