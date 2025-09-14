from pycsp3.problems.data.parsing import *
from pycsp3.problems.data.parsing import split_with_rows_of_size

nActs = number_in(line())
nResources = number_in(next_line())
nSkills = number_in(next_line())
nPrecs = number_in(next_line())
nUnavailable = number_in(next_line())
nUnrels = number_in(next_line())  # number of unrelated activites wrt to the precedence graph
data['horizon'] = number_in(next_line())  # maximum makespan

ln = next_line()
useful_ressources = decrement([[int(v) for v in tok.split(", ")] for tok in ln[ln.find("{") + 1:ln.rfind("}")].split("}, {")])
ln = next_line()
potential_acts = decrement([[int(v) for v in tok.split(", ")] for tok in ln[ln.find("{") + 1:ln.rfind("}")].split("}, {")])
costs = numbers_in(next_line())
durations = numbers_in(next_line())
skill_requirements = split_with_rows_of_size(numbers_in(next_line())[1:], nSkills)
ln = next_line()
skill_mastery = split_with_rows_of_size([1 if tok == "true" else 0 for tok in ln[ln.find('[') + 1:ln.rfind("]")].split(",")], nSkills)

pred = decrement(numbers_in(next_line()))
succ = decrement(numbers_in(next_line()))
assert nPrecs == len(pred) == len(succ)
data['precedences'] = [(pred[i], succ[i]) for i in range(nPrecs)]

unpred = decrement(numbers_in(next_line()))
unsucc = decrement(numbers_in(next_line()))
assert nUnrels == len(unpred) == len(unsucc)
data['unrelated_precedences'] = [(unpred[i], unsucc[i]) for i in range(nUnrels)]

required_mass = numbers_in(next_line())

assert nResources == len(potential_acts) == len(costs) == len(skill_mastery)
data['ressources'] = OrderedDict([("potential_activities", potential_acts), ("costs", costs), ("skill_mastery", skill_mastery)])

M = M = decrement(numbers_in(next_line()))
assert M == [0, 1]  # for the moment
ln = next_line()
comp_prod = decrement(split_with_rows_of_size([[int(v) for v in tok.split(", ")] for tok in ln[ln.find("{") + 1:ln.rfind("}")].split("}, {")], 2))
maxDiff = numbers_in(next_line())

assert len(M) == len(comp_prod) == len(maxDiff)
data['mass'] = OrderedDict([("M", M), ("comp_prod", comp_prod), ("maxDiff", maxDiff)])

nLocations = number_in(next_line())
locations = decrement(numbers_in(next_line()))
data['location_capacities'] = numbers_in(next_line())
occupancies = numbers_in(next_line())
assert nLocations == len(data['location_capacities'])

assert nActs == len(useful_ressources) == len(durations) == len(skill_requirements) == len(required_mass) == len(locations) == len(occupancies)
data['activities'] = OrderedDict(
    [("useful_resources", useful_ressources), ("durations", durations), ("skill_requirements", skill_requirements), ("required_mass", required_mass)
        , ("locations", locations), ("occupancies", occupancies)])

unavailable_resources = decrement(numbers_in(next_line()))
unavailable_starts = numbers_in(next_line())
unavailable_ends = numbers_in(next_line())
assert nUnavailable == len(unavailable_resources) == len(unavailable_starts) == len(unavailable_ends)
data['unavailable'] = OrderedDict([("resources", unavailable_resources), ("starts", unavailable_starts), ("ends", unavailable_ends)])
