"""
Problem 081 on CSPLib

## Data Illustration
  example.json

## Model
 constraints: Channel, Slide, Table

## Execution:
  python Blackhole.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob081/

## Tags
  recreational, notebook, csplib
"""

from pycsp3 import *

m, piles = data or load_json_data("example.json")  # m denotes the number of cards per suit

nCards = 4 * m

# x[i] is the value j of the card at the ith position of the built stack
x = VarArray(size=nCards, dom=range(nCards))

# y[j] is the position i of the card whose value is j
y = VarArray(size=nCards, dom=range(nCards))

T = {(i, j) for i in range(nCards) for j in range(nCards) if i % m == (j + 1) % m or j % m == (i + 1) % m}

satisfy(
    # linking variables of x and y
    Channel(x, y),

    # the Ace of Spades is initially put on the stack
    y[0] == 0,

    # cards must be played in the order of the piles
    [Increasing(y[pile], strict=True) for pile in piles],

    # each new card put on the stack must be at a rank higher or lower than the previous one
    Slide((x[i], x[i + 1]) in T for i in range(nCards - 1))
)

""" Comments
1) Slide is only used to have more compact XCSP3 instances
   we could have written: [(x[i], x[i + 1]) in T for i in range(nCards - 1)]  
2) Increasing(y[pile], strict=True)
 is equivalent to:
   Increasing([y[j] for j in pile], strict=True)
"""
