from pycsp3.problems.data.parsing import *

nConcerts = number_in(line())
starts = numbers_in(next_line())
ends = numbers_in(next_line())
prices = numbers_in(next_line())
nHalls = number_in(next_line())
data['capacities'] = numbers_in(next_line())
requirements = numbers_in(next_line())

assert nConcerts == len(starts) == len(ends) == len(prices) == len(requirements)
assert nHalls == len(data['capacities'])
data['concerts'] = [OrderedDict([("start", starts[i]), ("end", ends[i]), ("price", prices[i]), ("requirement", requirements[i])]) for i in range(nConcerts)]
