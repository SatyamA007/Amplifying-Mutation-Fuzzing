from fuzzingbook.MutationFuzzer import MutationFuzzer

seed_input = "http://www.google.com/search?q=fuzzing"
mutation_fuzzer = MutationFuzzer(seed=[seed_input])
seeds = [mutation_fuzzer.fuzz() for i in range(10)]
print(seeds)

