import time
import numpy as np
import matplotlib.pyplot as plt

from sample_programs.crash_me import crash_me
from fuzzingbook.GreyboxFuzzer import Mutator
from fuzzingbook.GreyboxFuzzer import FunctionCoverageRunner
from fuzzingbook.GreyboxFuzzer import AFLFastSchedule
from fuzzingbook.GreyboxFuzzer import CountingGreyboxFuzzer
from fuzzingbook.Coverage import population_coverage

if __name__ == "__main__":
        
    n = 50000
    seed_input = "good"
    fast_schedule = AFLFastSchedule(5)
    fast_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), fast_schedule)
    start = time.time()
    fast_fuzzer.runs(FunctionCoverageRunner(crash_me), trials=n)
    end = time.time()

    x_axis = np.arange(len(fast_schedule.path_frequency))
    y_axis = list(fast_schedule.path_frequency.values())

    time_taken = end - start
    _, boost_coverage = population_coverage(fast_fuzzer.inputs, crash_me)
    boosted_max_coverage = max(boost_coverage)
    print(f"The boosted fuzzer took {time_taken}s for a total coverage of {boosted_max_coverage}")

    line_boost, = plt.plot(boost_coverage, label="Boosted Greybox Fuzzer")
    plt.legend(handles=[line_boost])
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')
    plt.show()
