"""
The tank allocation problem involves the assignment of different cargoes (volumes of chemical products) to the available tanks of a vessel.
The constraints to satisfy are mainly segregation constraints:
  - prevent chemicals from being loaded into certain types of tanks
  - prevent some pairs of cargoes to be placed next to each other
An ideal loading plan should maximize the total volume of unused tanks (i.e. free space).

## Data
  chemical.json

## Model
  constraints: BinPacking, Sum, Table

## Execution
  python TankAllocation1.py -data=<datafile.json>
  python TankAllocation1.py -data=<datafile.json> -variant=bp
  python TankAllocation1.py -data=<datafile.json> -parser=TankAllocation_Converter.py
  python TankAllocation1.py -data=<datafile.txt> -parser=TankAllocation_Parser.py

## Links
  - https://www.csplib.org/Problems/prob051/models/
  - https://link.springer.com/article/10.1007/s10601-017-9278-x
  - https://link.springer.com/chapter/10.1007/978-3-642-33558-7_58
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
 """

from pycsp3 import *

assert not variant() or variant("bp")

volumes, conflicts, tanks = data or load_json_data("chemical.json")

capacities, impossible_cargos, neighbours = zip(*tanks)
nCargos, nTanks = len(volumes), len(tanks)

DUMMY_CARGO = nCargos
MAX = sum(capacities) + 1

sorted_capacities = sorted(capacities)
ranges = [range(number_of_values_for_sum_ge(sorted_capacities, volume, True), number_of_values_for_sum_ge(sorted_capacities, volume) + 1) for volume in volumes]

T = conflicts + [(v, u) for u, v in conflicts]

# x[i] is the cargo (type) of the ith tank (DUMMY_CARGO, if empty)
x = VarArray(size=nTanks, dom=range(nCargos + 1))

satisfy(
    # allocating a compatible cargo to each tank
    [x[i] not in impossible_cargos[i] for i in range(nTanks)],

    # ensuring no adjacent tanks containing incompatible cargo
    [(x[i], x[j]) not in T for i in range(nTanks) for j in neighbours[i]]
)

if not variant():
    satisfy(
        # ensuring each cargo is shipped
        [Sum(capacities[i] * (x[i] == cargo) for i in range(nTanks) if cargo not in impossible_cargos[i]) >= volumes[cargo] for cargo in range(nCargos)]
    )

    maximize(
        # maximizing free space
        Sum(capacities[i] * (x[i] == DUMMY_CARGO) for i in range(nTanks))
    )

elif variant("bp"):

    # ld[j] is volume (load) available for the jth cargo
    ld = VarArray(size=nCargos + 1, dom=lambda j: range(MAX) if j == DUMMY_CARGO else range(volumes[j], volumes[j] + max(capacities) + 1))

    satisfy(
        BinPacking(
            partition=x,
            sizes=capacities,
            loads=ld
        )
    )

    maximize(
        # maximizing free space
        ld[-1]
    )

"""
1) this redundant constraint seems to be counter-productive:
    # tag(redundant)
    Cardinality(
        within=x,
        occurrences={j: ranges[j] for j in range(nCargos)} | {nCargos: range(nTanks - sum(r.start for r in ranges) + 1)}
    )
"""

# maximize(
#     # maximising the number of empty tanks
#     Sum(x[i] == DUMMY_CARGO for i in range(nTanks))
# )
