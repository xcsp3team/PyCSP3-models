from pycsp3.problems.data.parsing import *

horizon = number_in(line())
nGenerators = number_in(next_line())
nLoads = number_in(next_line())
# next_line(repeat=1)
data['gen_max'] = [numbers_in(next_line()) for _ in range(nGenerators)]
data['dispatch_cost'] = [numbers_in(next_line()) for _ in range(nGenerators)]
data['gen_min'] = [numbers_in(next_line()) for _ in range(nGenerators)]
# next_line()
data['init_commitment'] = numbers_in(next_line())
data['startup_cost'] = numbers_in(next_line())
data['shutdown_cost'] = numbers_in(next_line())
data['max_ramp_rate'] = numbers_in(next_line())
# next_line()
data['demand'] = [numbers_in(next_line()) for _ in range(nLoads)]
data['shed_cost'] = numbers_in(next_line())
data['min_down'] = numbers_in(next_line())
data['max_num_start'] = numbers_in(next_line())
