"""
A number of cars are to be produced; they are not identical, because different options are available as variants on the basic model.
The assembly line has different stations which install the various options (air-conditioning, sunroof, etc.).
These stations have been designed to handle at most a certain percentage of the cars passing along the assembly line.
Furthermore, the cars requiring a certain option must not be bunched together, otherwise the station will not be able to cope.
Consequently, the cars must be arranged in a sequence so that the capacity of each station is never exceeded.
For instance, if a particular station can only cope with at most half of the cars passing along the line, the sequence must
be built so that at most 1 car in any 2 requires that option.

See problem 001 at CSPLib.

## Data Example
  dingbas.json

## Model
  Two variants manage differently the way assembled car options are computed:
  - a main variant involving logical constraints
  - a variant 'table' involving table constraints

  constraints: Cardinality, Sum, Table

## Execution
  python CarSequencing.py -data=<datafile.json>
  python CarSequencing.py -data=<datafile.json> -variant=table
  python CarSequencing.py -data=<datafile.txt> -parser=CarSequencing_Parser.py

## Links
  - https://www.csplib.org/Problems/prob001/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  realistic, csplib, xcsp22
"""

from pycsp3 import *
from math import ceil

assert not variant() or variant("table")

classes, limits = data or load_json_data("dingbas.json")

demands, options = zip(*classes)
nCars, nClasses, nOptions = sum(demands), len(classes), len(limits)


def indicators(k, nb):  # nb stands for the number of consecutive blocks (of several cars) set to their maximal capacity
    n_cars_with_option = sum(demand for (demand, opts) in classes if opts[k] == 1)
    remaining = n_cars_with_option - nb * limits[k].num
    possible = nCars - nb * limits[k].den
    return remaining, possible


# c[i] is the class of the ith assembled car
c = VarArray(size=nCars, dom=range(nClasses))

# o[i][k] is 1 if the ith assembled car has option k
o = VarArray(size=[nCars, nOptions], dom={0, 1})

satisfy(
    # building the right numbers of cars per class
    Cardinality(
        within=c,
        occurrences=demands
    )
)

if not variant():
    satisfy(
        # computing assembled car options
        If(
            c[i] == j,
            Then=o[i] == options[j]
        ) for i in range(nCars) for j in range(nClasses)
    )

elif variant("table"):
    satisfy(
        # computing assembled car options
        Table(
            scope=(c[i], o[i]),
            supports=enumerate(options)
        ) for i in range(nCars)
    )

satisfy(
    # respecting option frequencies
    [
        Sum(o[i:i + den, k]) <= num
        for k, (num, den) in enumerate(limits) for i in range(nCars) if i <= nCars - den
    ],

    # additional constraints by reasoning from consecutive blocks
    # tag(redundant)
    [
        Sum(o[:possible, k]) >= remaining
        for k in range(nOptions) for nb in range(ceil(nCars // limits[k].den) + 1)
        if (res := indicators(k, nb)) and ((remaining := res[0]) > 0) and ((possible := res[1]) > 0)
    ]
)

""" Comments
1) the table variant seems far more efficient
2) (c[i], o[i]) is a possible shortcut for (c[i], *o[i])
3) the redundant constraints seem important
4) Note that:
 Cardinality(c, occurrences=demands)
   is a shortcut for:
 Cardinality(c, occurrences={j: demands[j] for j in range(nClasses)})
5) It is no more possible to write directly (ie. using enumerate for posting a table with operator 'in"):
 (c[i], o[i]) in enumerate(options) for i in range(nCars)
 Table constraints must be posted with:
   - the function Table as in the model
   - or with the operator in and a right operand which is a list or set of tuples   
WARNING: tuples are flattened when necessary
6) Note that:
 If(c[i] == j, Then=o[i] == opts) for i in range(nCars) for j, (_, opts) in enumerate(classes)
    is a shortcut for:
 If(c[i] == j, Then=o[i][k] == options[j][k]) for i in range(nCars) for j in range(nClasses) for k in range(nOptions) 
WARNING: the compilation, although equivalent can produce different outputs (which one is better?)
"""
