"""
Arrange an array such that the average of 2 numbers does not lie between them.

## Data Example
  pic.json

## Model
  constraints: AllDifferent, Minimum

## Execution
  python AverageAvoiding.py -data=<datafile.json>
  python AverageAvoiding.py -data=<datafile.json> -variant=mini

## Links
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
"""

from pycsp3 import *
from collections import Counter

# NB : actually this is equivalent to range(100)
pic = [0, 64, 96, 32, 48, 80, 16, 56, 88, 24, 40, 72, 60, 92, 8, 28, 44, 76, 12, 52, 84, 20, 36, 68, 62, 94, 4, 30, 46, 78, 14, 54, 86, 22, 38, 70, 58, 90, 6,
       26, 42, 74, 10, 50, 82, 98, 18, 34, 66, 2, 1, 65, 97, 33, 49, 81, 17, 57, 89, 25, 41, 73, 61, 93, 9, 29, 45, 77, 13, 53, 85, 21, 37, 69, 63, 95, 5, 31,
       47, 79, 15, 55, 87, 23, 39, 71, 59, 91, 7, 27, 43, 75, 11, 51, 83, 99, 19, 35, 67, 3]

sequence = pic if isinstance(data, int) and data == 0 else list(range(data)) if isinstance(data, int) else data

d = Counter(sequence)
n = len(sequence)

# x[i] is the ith value of the sequence
x = VarArray(size=n, dom=set(d.keys()))

if not variant():

    satisfy(
        # ensuring that the average of 2 numbers of the sequence separated by a value v is not v
        [2 * x[k] != x[i] + x[j] for i, j in combinations(n, 2) if i + 1 < j for k in range(i + 1, j)],

        # ensuring that we have a permutation of the initial sequence
        AllDifferent(x),
        # Cardinality(x, occurrences={k: v for k, v in d.items()}),

        # tag(symmetry-breaking)
        x[0] == Minimum(x)
    )

elif variant("mini"):

    # y[i] is the ith value of the sequence, multiplied by 2
    y = VarArray(size=n, dom={2 * v for v in set(d.keys())})

    satisfy(
        # computing auxiliary variables
        [y[i] == 2 * x[i] for i in range(n)],

        # ensuring that the average of 2 numbers of the sequence separated by a value v is not v
        [y[k] != x[i] + x[j] for i, j in combinations(n, 2) if i + 1 < j for k in range(i + 1, j)],

        # ensuring that we have a permutation of the initial sequence
        AllDifferent(x),

        # tag(symmetry-breaking)
        [x[0] <= x[i] for i in range(1, n)]
    )

""" Comments
1) We should be able to post Cardinality while being able to recognize a AllDif at compîlation time when it is the case
2) TODO use -1 instead of 0 and fix the problem data=-1 => we get a str instead of an int
3) Data used for the 2024 Competition: [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
"""
