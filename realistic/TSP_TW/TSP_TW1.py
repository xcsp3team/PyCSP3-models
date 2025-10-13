"""
The Traveling Salesman Problem with Time Windows (TSPTW) is a popular variant of the TSP where the salesman’s customers
must be visited within given time windows.
See IJCAI paper below.

## Data Example
  n020w020-1.json

## Model
  constraints: AllDifferent, Element, Sum

## Execution
  python TSP_TW1.py -data=<datafile.json>
  python TSP_TW1.py -data=<datafile.txt> -parser=TSP_TW_Parser.py

## Links
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

distances, windows = data or load_json_data("n020w020-1.json")

Earliest, Latest = cp_array(zip(*windows))
horizon = max(Latest) + 1

n = len(distances)
N = range(n)

# x[i] is the customer (node) visited in the ith position
x = VarArray(size=n + 1, dom=range(n))

# a[i] is the time when is visited the customer in the ith position
a = VarArray(size=n, dom=range(horizon))

satisfy(
    #  making it a tour while starting and ending at city 0
    [
        x[0] == 0,
        x[-1] == 0,
        a[0] == 0
    ],

    AllDifferent(x[:-1]),

    # enforcing time windows
    [
        [Earliest[x[i]] <= a[x[i]] for i in N],

        [a[x[i]] <= Latest[x[i]] for i in N],

        [a[x[i + 1]] >= a[x[i]] + distances[x[i], x[i + 1]] for i in N[:-1]]
    ]
)

minimize(
    # minimizing travelled distance
    Sum(distances[x[i], x[(i + 1) % n]] for i in N)
)
