from pycsp3.problems.data.parsing import *
from enum import Enum, auto


def aut(n_occurrences=1):
    return auto() if n_occurrences == 1 else (auto() for _ in range(n_occurrences))


class AGE(Enum):
    BABY, CHILD, YOUTH, ADULT, SENIOR, AGED, ANCIENT = aut(7)


class GENDER(Enum):
    FEMALE, MALE, OTHER = aut(3)


class HEALTH(Enum):
    GOOD, POOR, COMPROMISED = aut(3)


class EXPOSURE(Enum):
    LOW, AVERAGE, HIGH, EXTREME = aut(4)


lb, nVaccines = numbers_in(line())
assert lb == 1
data['nVaccines'] = nVaccines
m = number_in(next_line())
line = next_line()
ages = [AGE[tok].value for tok in line[line.index("[") + 1:line.rindex("]")].split(", ")]  # not -1 for ages (for keeping special value 0)
line = next_line()
genders = [GENDER[tok].value - 1 for tok in line[line.index("[") + 1:line.rindex("]")].split(", ")]
line = next_line()
healths = [HEALTH[tok].value - 1 for tok in line[line.index("[") + 1:line.rindex("]")].split(", ")]
line = next_line()
exposures = [EXPOSURE[tok].value - 1 for tok in line[line.index("[") + 1:line.rindex("]")].split(", ")]
sizes = numbers_in(next_line())
assert m == len(ages) == len(genders) == len(healths) == len(exposures) == len(sizes)
data['groups'] = [OrderedDict([("age", ages[i]), ("gender", genders[i]), ("health", healths[i]), ("exposure", exposures[i]), ("size", sizes[i])]) for i in
                  range(m)]
minsize = number_in(next_line())
age_group_mins = numbers_in(next_line())
age_group_maxs = numbers_in(next_line())
assert len(AGE) == len(age_group_mins) == len(age_group_maxs)
data['ageBounds'] = [OrderedDict([("lb", age_group_mins[i]), ("ub", age_group_maxs[i])]) for i in range(len(AGE))]

max_diff = number_in(next_line())
max_share = number_in(next_line())
data['limits'] = OrderedDict([("minSize", minsize), ("maxDiff", max_diff), ("maxShare", max_share)])

health_information = numbers_in(next_line())
exposure_information = numbers_in(next_line())
assert len(HEALTH) == len(health_information) and len(EXPOSURE) == len(exposure_information)

data['information'] = OrderedDict([("health", health_information), ("exposure", exposure_information)])

# s = "{Vaccine(5), Vaccine(6)}, {Vaccine(3), Vaccine(4), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2)}, {Vaccine(1), Vaccine(2), Vaccine(3), Vaccine(4)}, {Vaccine(1), Vaccine(2), Vaccine(3), Vaccine(4), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2), Vaccine(3), Vaccine(4)}, {Vaccine(1), Vaccine(2), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2), Vaccine(5), Vaccine(6)}, {Vaccine(3), Vaccine(4)}, {Vaccine(3), Vaccine(4), Vaccine(5), Vaccine(6)}, {Vaccine(3), Vaccine(4), Vaccine(5), Vaccine(6)}, {Vaccine(1), Vaccine(2), Vaccine(3), Vaccine(4)}, {Vaccine(1), Vaccine(2), Vaccine(3), Vaccine(4)}, {Vaccine(3), Vaccine(4), Vaccine(5), Vaccine(6)}"
# m = [decrement(numbers_in(tok)) for tok in s.split("}, {")]
# m = [[1 if j in t else 0 for j in range(nVaccines)] for t in m]
