import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from fuzzingbook.GreyboxFuzzer import Mutator
from fuzzingbook.GreyboxFuzzer import FunctionCoverageRunner
from fuzzingbook.GreyboxFuzzer import AFLFastSchedule
from fuzzingbook.GreyboxFuzzer import CountingGreyboxFuzzer
from fuzzingbook.Coverage import population_coverage
from utils import *

if __name__ == "__main__":
    program_num = '1'
    if len(sys.argv)>1:
        program_num = str(sys.argv[1])
                
    n = 10000
    seed_input = "good"
    fast_schedule = AFLFastSchedule(5)
    fast_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), fast_schedule)
    start = time.time()
    fast_fuzzer.runs(FunctionCoverageRunner(programs[program_num]['function']), trials=n)
    end = time.time()

    x_axis = np.arange(len(fast_schedule.path_frequency))
    y_axis = list(fast_schedule.path_frequency.values())

    time_taken = end - start
    _, boost_coverage = population_coverage(fast_fuzzer.inputs, programs[program_num]['function'])
    boosted_max_coverage = max(boost_coverage)
    print(f"The boosted fuzzer took {time_taken}s for a total coverage of {boosted_max_coverage}")

    line_boost, = plt.plot(boost_coverage, label="Boosted Greybox Fuzzer")
    plt.legend(handles=[line_boost])
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')
    plt.show()
