"""
The Traveling Salesman Problem with Time Windows (TSPTW) is a popular variant of the TSP where the salesman’s customers
must be visited within given time windows.
See IJCAI paper below.

## Data Example
  n020w020-1.json

## Model
  constraints: Circuit, Element, Sum

## Execution
  python TSP_TW2.py -data=<datafile.json>
  python TSP_TW2.py -data=<datafile.txt> -parser=TSP_TW_Parser.py

## Links
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

distances, windows = data
horizon = max(latest for (_, latest) in windows) + 1
n = len(distances)

# x[i] is the node succeeding to the ith node
x = VarArray(size=n, dom=range(n))

# a[i] is the time when is visited the ith node
a = VarArray(size=n, dom=lambda i: range(windows[i][0], windows[i][1] + 1))

satisfy(
    #  making it a tour while starting and ending at city 0
    a[0] == 0,

    # avoiding self-loops
    [x[i] != i for i in range(n)],

    # forming a circuit
    Circuit(x),

    # enforcing time windows
    [
        If(
            x[i] != 0,
            Then=a[x[i]] >= a[i] + distances[i][x[i]]
        ) for i in range(n)
    ]
)

minimize(
    # minimizing travelled distance
    Sum(distances[i, x[i]] for i in range(n))
)
