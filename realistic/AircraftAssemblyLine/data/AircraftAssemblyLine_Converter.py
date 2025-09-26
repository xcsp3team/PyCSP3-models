import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# Example: python AircraftAssemblyLine.py -data=test.json -parser=AircraftAssemblyLine_Converter.py [-export]

name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

nAreas = d.get("nAreas")
areasCapacities = d.get("areasCapacities")
tasksPerAreas = d.get("tasksPerAreas")

nStations = d.get("nStations")
machines = d.get("machines")
nMaxOpsPerStation = d.get("nMaxOpsPerStation")

nTasks = d.get("nTasks")
durations = d.get("durations")
operators = d.get("operators")
usedAreaRooms = d.get("usedAreas")
neutralizedAreas = d.get("neutralizedAreas")

data['takt'] = d.get("takt")
assert nAreas == len(areasCapacities) == len(tasksPerAreas)
data["areas"] = [OrderedDict([("capacity", areasCapacities[i]), ("tasks", tasksPerAreas[i])]) for i in range(nAreas)]
assert nStations == len(machines) == len(nMaxOpsPerStation)
data["stations"] = [OrderedDict([("machines", machines[i]), ("maxOperators", nMaxOpsPerStation[i])]) for i in range(nStations)]
assert nTasks == len(durations) == len(operators) == len(usedAreaRooms) == len(neutralizedAreas)
data["tasks"] = [OrderedDict([("duration", durations[i]), ("nOperators", operators[i]), ("usedAreaRooms", usedAreaRooms[i]),
                              ("neutralizedAreas", neutralizedAreas[i])]) for i in range(nTasks)]
data["tasksPerMachine"] = d.get("tasksPerMachine")
data["precedences"] = d.get("precedences")

pos = name.rfind("/")
Compilation.string_data = "-" + name[pos + 1:] if pos != -1 else name
