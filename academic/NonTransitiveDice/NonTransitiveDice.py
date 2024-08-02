"""
A set of dice is intransitive if the binary relation “X rolls a higher number than Y more than half the time” on its elements is not transitive.
This situation is similar to that in the game Rock, Paper, Scissors, in which each element has an advantage over one choice and a disadvantage to the other.
The problem is to exhibit such a set of dice.

## Data
  three integers: n, m and d

## Model
  constraints: Maximum, Sum

## Execution
  python NonTransitiveDice.py -data=[number,number,number]
  python NonTransitiveDice.py -data=[number,number,number] -variant=opt

## Links
  - https://en.wikipedia.org/wiki/Intransitive_dice
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

n, m, d = data or (6, 6, 0)  # number of dice, number of sides of each die, and number of possible values
d = 2 * m if d == 0 else d  # computing the number of possible values if necessary

# x[i][j] is the value of the jth face of the ith die
x = VarArray(size=[n, m], dom=range(d))

# y[i] is the number of winnings of the ith die against the i+1th die (first value) and vice versa (second value)
y = VarArray(size=[n, 2], dom=range(m * m + 1))

# gap[i] is the dominance gap of the ith die
gap = VarArray(size=n, dom=range(1, m * m + 1))

# z is the maximal value of a die
z = Var(dom=range(d))

satisfy(
    # ordering numbers on each die  tag(symmetry-breaking)
    [Increasing(x[i]) for i in range(n)],

    # computing dominance
    [
        (
            y[i][0] == Sum(x[i][r1] > x[i + 1][r2] for r1 in range(m) for r2 in range(m)),
            y[i][1] == Sum(x[i + 1][r1] > x[i][r2] for r1 in range(m) for r2 in range(m))
        ) for i in range(n)
    ],

    # computing dominance gap
    [gap[i] == y[i][0] - y[i][1] for i in range(n)],

    # computing z
    z == Maximum(x)
)

if variant("opt"):
    minimize(
        #  minimize the maximal gap
        Maximum(gap) * 1000 + z
    )

""" Comments
0) index auto-indexing is active by default:  x[i + 1] is equal to x[(i + 1) % n]
1) no need for posting:
   # ensuring non-transitivity
   [y[i][0] > y[i][1] for i in range(n)],
   as the domain of gap variables start at 1
2) for being compatible with the competition CSP mini-track, we:
   discard z
   [x[i][j] <= x[i][j + 1] for i in range(n) for j in range(m - 1)],
   #[Increasing(x[i]) for i in range(n)],
"""
