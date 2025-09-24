"""
The tank allocation problem involves the assignment of different cargoes (volumes of chemical products) to the available tanks of a vessel.
The constraints to satisfy are mainly segregation constraints:
  - prevent chemicals from being loaded into certain types of tanks
  - prevent some pairs of cargoes to be placed next to each other
An ideal loading plan should maximize the total volume of unused tanks (i.e. free space).

## Data
  chemical.json

## Model
  constraints: AllDifferent, Count Sum, Table

## Execution
  python TankAllocation2.py -data=<datafile.json>
  python TankAllocation2.py -data=<datafile.json> -parser=TankAllocation_Converter.py
  python TankAllocation2.py -data=<datafile.txt> -parser=TankAllocation_Parser.py

## Links
  - https://www.csplib.org/Problems/prob051/models/
  - https://link.springer.com/article/10.1007/s10601-017-9278-x
  - https://link.springer.com/chapter/10.1007/978-3-642-33558-7_58
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

from pycsp3.tools.utilities import number_of_values_for_sum_ge

volumes, conflicts, tanks = data
capacities, impossible_cargos, neighbours = zip(*tanks)
nCargos, nTanks = len(volumes), len(tanks)
conflicts = [(i, j) for i, j in conflicts if volumes[i] > 0 and volumes[j] > 0]
# assert all(volumes[i] > 0 and volumes[j] > 0 for i, j in conflicts)

sorted_capacities = sorted(list(enumerate(capacities)), key=lambda v: v[1])
nMaxTanks = [number_of_values_for_sum_ge(sorted(capacities), volume) for volume in volumes]
impossible_tanks = [[j for j in range(nTanks) if i in impossible_cargos[j]] for i in range(nCargos)]
DUMMY_TANK = -1

C = [i for i in range(nCargos) if volumes[i] != 0]  # relevant cargos
A = sorted(list(set([(i, j) for i in range(nTanks) for j in neighbours[i]] + [(j, i) for i in range(nTanks) for j in neighbours[i]])))


def T(cargo):
    def rec_f(volume, tab, tmp, cursor_cap, cursor_tmp):
        for j in range(cursor_cap, nTanks):
            tmp[cursor_tmp] = sorted_capacities[j]
            if sum(tmp[k][1] for k in range(cursor_tmp + 1)) >= volume:
                tab.append(tuple(tmp[k][0] if k <= cursor_tmp else DUMMY_TANK for k in range(len(tmp))))
            else:
                rec_f(volume, tab, tmp, j + 1, cursor_tmp + 1)
        return tab

    return rec_f(volumes[cargo], [], [DUMMY_TANK] * nMaxTanks[cargo], 0, 0)


# x[i][k] is the kth tank used for the ith cargo (-1, if not used)
x = VarArray(size=[nCargos, max(nMaxTanks)], dom=lambda i, k: None if volumes[i] == 0 or k >= nMaxTanks[i] else range(-1, nTanks))

# y[j] is 1 if the jth tank is used
y = VarArray(size=nTanks, dom={0, 1})

satisfy(
    # using compatible tanks for each cargo
    [x[i][k] not in impossible_tanks[i] for i in C for k in range(nMaxTanks[i])],

    # using different tanks
    AllDifferent(x, excepting=-1),

    # ensuring each cargo is shipped
    [x[i] in T(i) for i in C],

    # ensuring no adjacent tanks containing incompatible cargo
    [(x[i][k], x[j][q]) not in A for i, j in conflicts for k in range(nMaxTanks[i]) for q in range(nMaxTanks[j])],

    # computing if tanks are used
    [Exist(x, value=j, reified_by=y[j]) for j in range(nTanks)] if variant("reif")
    else [y[j] == (j in flatten(x)) for j in range(nTanks)]
)

maximize(
    # maximizing free space
    Sum(capacities[j] * (y[j] == 0) for j in range(nTanks))
)

# # tag(symmetry-breaking)  TODO this is not correct considering the way tables are built
# [Decreasing(x[i]) for i in C],
