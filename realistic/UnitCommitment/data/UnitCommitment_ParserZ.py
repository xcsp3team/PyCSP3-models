from pycsp3.problems.data.parsing import *

horizon = number_in(line())
nGenerators = number_in(next_line())
nLoads = number_in(next_line())
# next_line(repeat=1)
gen_max = [numbers_in(next_line()) for _ in range(nGenerators)]
dispatch_costs = [numbers_in(next_line()) for _ in range(nGenerators)]
gen_min = [numbers_in(next_line()) for _ in range(nGenerators)]
# next_line()
init_commitments = numbers_in(next_line())
startup_costs = numbers_in(next_line())
shutdown_costs = numbers_in(next_line())
max_ramp_rates = numbers_in(next_line())
# next_line()
demands = [numbers_in(next_line()) for _ in range(nLoads)]
shedding_costs = numbers_in(next_line())
min_downtimes = numbers_in(next_line())
max_startups = numbers_in(next_line())

assert nGenerators == len(init_commitments) == len(startup_costs) == len(shutdown_costs) == len(max_ramp_rates) == len(min_downtimes) == len(max_startups)
assert nLoads == len(shedding_costs)
assert all(horizon == len(t) for m in (gen_min, gen_max, dispatch_costs, demands) for t in m)

data['generators'] = OrderedDict(
    [("min_capacities", gen_min), ("max_capacities", gen_max), ("dispatch_costs", dispatch_costs), ("init_commitment", init_commitments),
     ("startup_costs", startup_costs), ("shutdown_costs", shutdown_costs), ("max_ramp_rates", max_ramp_rates), ("min_downtimes", min_downtimes),
     ("max_startups", max_startups)])
data['loads'] = OrderedDict([("demands", demands), ("shedding_costs", shedding_costs)])
