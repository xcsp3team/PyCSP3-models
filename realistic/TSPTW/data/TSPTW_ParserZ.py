from pycsp3.problems.data.parsing import *

nLocations = number_in(next_line())
data['durations'] = [numbers_in(next_line()) for _ in range(nLocations)]
data['early_times'] = numbers_in(next_line())
data['late_times'] = numbers_in(next_line())
assert len(data['durations']) == len(data['early_times']) == len(data['late_times'])
