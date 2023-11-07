""""
A number of cars are to be produced; they are not identical, because different options are available as variants on the basic model.
The assembly line has different stations which install the various options (air-conditioning, sun-roof, etc.).
These stations have been designed to handle at most a certain percentage of the cars passing along the assembly line.
Furthermore, the cars requiring a certain option must not be bunched together, otherwise the station will not be able to cope.
Consequently, the cars must be arranged in a sequence so that the capacity of each station is never exceeded.
For instance, if a particular station can only cope with at most half of the cars passing along the line, the sequence must
be built so that at most 1 car in any 2 requires that option.


## Data (example)
  dingbas.json

## Model
  Two variants manage differently the way assembled car options are computed:
  - a main variant involving logical constraints
  - a variant 'table' involving  table constraints

  constraints: Cardinality, Intension, Extension, Sum

## Execution
  - python CarSequencing.py -data=dingbas.json
  - python CarSequencing.py -variant=table -data=dingbas.json

## Links
  - https://www.csplib.org/Problems/prob001/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  real, xcsp22
"""

from pycsp3 import *
from math import ceil

classes, limits = data
demands = [demand for demand, _ in classes]
nCars, nClasses, nOptions = sum(demands), len(classes), len(limits)


def sum_from_full_consecutive_blocks(k, nb):
    # nb stands for the number of consecutive blocks (of several cars) set to their maximal capacity
    n_cars_with_option = sum(demand for (demand, options) in classes if options[k] == 1)
    remaining = n_cars_with_option - nb * limits[k].num
    possible = nCars - nb * limits[k].den
    return Sum(o[:possible, k]) >= remaining if remaining > 0 and possible > 0 else None


# c[i] is the class of the ith assembled car
c = VarArray(size=nCars, dom=range(nClasses))

# o[i][k] is 1 if the ith assembled car has option k
o = VarArray(size=[nCars, nOptions], dom={0, 1})

satisfy(
    # building the right numbers of cars per class
    Cardinality(c, occurrences={j: demands[j] for j in range(nClasses)})
)

if not variant():
    satisfy(
        # computing assembled car options
        imply(c[i] == j, o[i][k] == options[k]) for i in range(nCars) for j, (_, options) in enumerate(classes) for k in range(nOptions)
    )
elif variant("table"):
    satisfy(
        # computing assembled car options
        (c[i], *o[i]) in {(j, *options) for j, (_, options) in enumerate(classes)} for i in range(nCars)
    )

satisfy(
    # respecting option frequencies
    [Sum(o[i:i + den, k]) <= num for k, (num, den) in enumerate(limits) for i in range(nCars) if i <= nCars - den],

    # additional constraints by reasoning from consecutive blocks  tag(redundant-constraints)
    [sum_from_full_consecutive_blocks(k, nb) for k in range(nOptions) for nb in range(ceil(nCars // limits[k].den) + 1)]
)

""" Comments
1) the table variant seems far more efficient
2) (c[i], o[i]) is a possible shortcut for (c[i], *o[i])
3) the redundant constraints seem very important
"""
