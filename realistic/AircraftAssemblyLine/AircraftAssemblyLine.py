"""
This problem has been proposed by Stéphanie Roussel from ONERA (Toulouse), and comes from an aircraft manufacturer.
The objective is to schedule tasks on an aircraft assembly line in order to minimize the overall number of operators required on the line.
The schedule must satisfy several operational constraints, the main ones being:
- tasks are assigned on a unique workstation (on which specific machines are available);
- the takt-time, i.e. the duration during which the aircraft stays on each workstation, must be respected;
- capacity of aircraft zones in which operators perform the tasks must never be exceeded;
- zones can be neutralized by some tasks, i.e. it is not possible to work in those zones during the tasks execution.

This model has been co-developed by teams of ONERA and CRIL.

## Data Example
  2-178-70-2.json

## Model
  constraints: Cumulative, NoOverlap, Sum

## Execution
  python AircraftAssemblyLine.py -data=<datafile.json>
  python AircraftAssemblyLine.py -data=<xcsp23/datafile.json> -parser=AircraftAssemblyLine_Converter.py

## Links
  - https://drops.dagstuhl.de/opus/frontdoor.php?source_opus=19069
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

takt, areas, stations, tasks, tasksPerMachine, precedences = data
nAreas, nStations, nTasks, nMachines = len(areas), len(stations), len(tasks), len(tasksPerMachine)

areaCapacities, areaTasks = zip(*areas)  # number of operators who can work, and tasks per area
stationMachines, stationMaxOperators = zip(*stations)
durations, operators, usedAreaRooms, neutralizedAreas = zip(*tasks)
usedAreas = [set(j for j in range(nAreas) if usedAreaRooms[i][j] > 0) for i in range(nTasks)]


def station_of_task(i):
    r = next((j for j in range(nMachines) if i in tasksPerMachine[j]), -1)
    return -1 if r == -1 else next(j for j in range(nStations) if stationMachines[j][r] == 1)


stationOfTasks = [station_of_task(i) for i in range(nTasks)]  # station of the ith task (-1 if it can be everywhere)

# x[i] is the starting time of the ith task
x = VarArray(size=nTasks, dom=range(takt * nStations + 1))

# z[j] is the number of operators at the jth station
z = VarArray(size=nStations, dom=lambda i: range(stationMaxOperators[i] + 1))

satisfy(
    # respecting the final deadline
    [x[i] + durations[i] <= takt * nStations for i in range(nTasks)],

    # ensuring that tasks start and finish in the same station
    [x[i] // takt == (x[i] + max(0, durations[i] - 1)) // takt for i in range(nTasks) if durations[i] != 0],

    # ensuring that tasks are put on the right stations (wrt needed machines)
    [x[i] // takt == stationOfTasks[i] for i in range(nTasks) if stationOfTasks[i] != -1],

    # respecting precedence relations
    [x[i] + durations[i] <= x[j] for (i, j) in precedences],

    # respecting limit capacities of areas
    [
        Cumulative(
            tasks=[Task(origin=x[t], length=durations[t], height=usedAreaRooms[t][i]) for t in areaTasks[i]]
        ) <= areaCapacities[i] for i in range(nAreas) if len(areaTasks[i]) > 1
    ],

    # computing/restricting the number of operators at each station
    [
        Cumulative(
            tasks=[Task(origin=x[t], length=durations[t], height=operators[t] * (x[t] // takt == j)) for t in range(nTasks)]
        ) <= z[j] for j in range(nStations)
    ],

    # no overlap (is there a better way to handle that?)
    [
        NoOverlap(
            tasks=[
                (x[i], durations[i]),
                (x[j], durations[j])
            ]
        ) for i in range(nTasks) for j in range(nTasks) if i != j and len(usedAreas[i].intersection(neutralizedAreas[j])) > 0
    ],

    # avoiding tasks using the same machine to overlap
    [
        NoOverlap(
            tasks=[(x[j], durations[j]) for j in tasksPerMachine[i]]
        ) for i in range(nMachines)
    ]
)

minimize(
    # minimizing the number of operators
    Sum(z)
)

# x == [0, 0, 109, 127, 127, 147, 152, 184, 0, 462, 184, 152, 387, 452, 394, 194, 186, 781, 202, 596, 596, 186, 186, 371, 0, 2160, 1660, 1620, 2080, 2120,
#       1700, 1740, 2290, 1920, 2160, 0, 1620, 1530, 1440, 0, 3646, 2190, 2290, 2880, 2880, 3258, 3258, 2350, 2783, 2708, 2608, 2350, 2425, 2500, 0, 4320,
#       3580, 3180, 2880, 3950, 3920, 3550, 0, 2350, 1920, 1760, 1760, 2190, 1740, 1900, 0, 4140, 1620, 2880, 1620, 2880, 1530, 2880, 2575, 2873, 2783, 2575,
#       0, 1311, 971, 971, 0, 971, 781, 781, 0, 3650, 2880, 2880, 3180, 3250, 0, 4870, 3646, 3646, 4320, 4320, 0, 5360, 4580, 5040, 0, 5270, 4870, 4870, 0,
#       5760, 4320, 4320, 4900, 4580, 5580, 5670, 202, 452, 556, 596, 596, 716, 716, 0, 2873, 836, 836, 956, 971, 1156, 1171, 1440, 2060, 1570, 2683, 4216,
#       5740, 5600, 5490, 5110, 5520, 5390, 5490, 5600, 4730, 5270, 5380, 5500, 4320, 4890, 5410, 4510, 5280, 5630, 4216, 5720, 5380, 5490, 4850, 5270, 5380,
#       5170, 5600, 4700, 4320, 4430, 5300, 4540, 4920, 5470, 5080, 5270, 5610, 4136, 5470, 4216, 4140, 4156, 4266, 4140, 4278, 4152, 4168, 4278, 4294, 4136,
#       4156, 5360, 4266, 4156, 4140, 4282, 3650, 4216, 3666, 3666, 3666],
# nOps == (4,6,8,6),

# Ace: using -di=0 -ale=4 ?
