from pycsp3.problems.data.parsing import *


def booleans_in(line, space=False):
    assert line is not None
    return [1 if tok == "true" else 0 for tok in line[line.index("[") + 1:line.rindex("]")].split("," + (" " if space else ""))]


data['nDepartments'] = number_in(line())
next_line()  # departmentName
nStations = number_in(next_line()) + 1  # +1
next_line()  # stationName
stationDepartments = numbers_in(next_line())[2:]
stationCommons = booleans_in(next_line())
assert nStations == len(stationDepartments) == len(stationCommons)
data["stations"] = [OrderedDict([("dpt", stationDepartments[i]), ("common", stationCommons[i])]) for i in range(nStations)]

nShifts = number_in(next_line()) + 1  # +1
next_line()  # shiftName
indexNight = numbers_in(next_line())
assert len(indexNight) == 0  # for the current data
shiftLengths = numbers_in(next_line())[2:]
l = next_line()
forbiddenSequences = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("},{")]
assert nShifts == len(shiftLengths) == len(forbiddenSequences)
data["shifts"] = [OrderedDict([("length", shiftLengths[i]), ("forbidden", forbiddenSequences[i])]) for i in range(nShifts)]

preferenceWeight = number_in(next_line())
riskWeight = number_in(next_line())
rbWeight = number_in(next_line())
persWeight = number_in(next_line())
stationWeight = number_in(next_line())
data["weights"] = OrderedDict([("preference", preferenceWeight), ("risk", riskWeight), ("rb", rbWeight), ("person", persWeight), ("station", stationWeight)])

data['nSkills'] = number_in(next_line()) + 1  # +1
next_line()  # skillName

nSubsums = number_in(next_line())
subDepartments = numbers_in(next_line())
l = next_line()
subSkills = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("}, ")]
nDays = number_in(next_line())
data['demands'] = split_with_structure(numbers_in(next_line())[5:], nStations, nShifts, nDays)
subDemands = split_with_rows_of_size(numbers_in(next_line())[3:], nDays)
assert nSubsums == len(subDepartments) == len(subSkills) == len(subDemands)
data["subsums"] = [OrderedDict([("dpt", subDepartments[i]), ("skills", subSkills[i]), ("demands", subDemands[i])]) for i in range(nSubsums)]

nPersons = number_in(next_line())
next_line()  # personName
stationPrefs = split_with_structure(numbers_in(next_line())[4:], nPersons, nStations)
persRobustness = numbers_in(next_line())  # not used
persRequireWork = booleans_in(next_line())
persRisk = booleans_in(next_line())
maxHoursWeek = numbers_in(next_line())
l = next_line()
forbiddenDays = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("}, {")]
histConsecutiveWorkDays = numbers_in(next_line())
histLastStationWorked = numbers_in(next_line())
histShiftLastDay = numbers_in(next_line())

assert nPersons == len(stationPrefs) == len(persRobustness) == len(persRequireWork)
assert nPersons == len(persRisk) == len(maxHoursWeek) == len(forbiddenDays)
assert nPersons == len(histConsecutiveWorkDays) == len(histLastStationWorked) == len(histShiftLastDay)

assert all(v == 0 for v in histConsecutiveWorkDays)  # for the current data
data["persons"] = [OrderedDict([("preferences", stationPrefs[i]), ("requiredWork", persRequireWork[i]), ("atRisk", persRisk[i]),
                                ("maxHoursPerWeek", maxHoursWeek[i]), ("forbiddenDays", forbiddenDays[i]), ("histDays", histConsecutiveWorkDays[i]),
                                ("histStation", histLastStationWorked[i]), ("histShift", histShiftLastDay[i])]) for i in range(nPersons)]
