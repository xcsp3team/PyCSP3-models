from pycsp3.problems.data.parsing import *

nCargos = number_in(line())
nTanks = number_in(next_line())
next_line()
capacities = [number_in(next_line()) for _ in range(nTanks)]
next_line(repeat=1)
neighbours = decrement([numbers_in(next_line()) for _ in range(nTanks)])
next_line(repeat=1)
impossible_cargos = decrement([numbers_in(next_line()) for _ in range(nTanks)])
next_line(repeat=1)
volumes = [number_in(next_line()) for _ in range(nCargos)]
next_line(repeat=2)
conflicts = decrement([numbers_in(ln) for ln in remaining_lines()])

data['volumes'] = volumes
data['conflicts'] = conflicts
data["tanks"] = [OrderedDict([("capacity", capacities[i]), ("impossibleCargos", impossible_cargos[i]), ("neighbors", neighbours[i])]) for i in range(nTanks)]
