"""
Cookie Monster Problem (by Richard Green)

Suppose that we have a number of cookie jars, each containing a certain number of cookies.
The Cookie Monster (CM) wants to eat all the cookies, but he is required to do so in a number
of sequential moves. At each move, the CM chooses a subset of the jars,
and eats the same (nonzero) number of cookies from each jar. The goal of the CM is to
empty all the cookies from the jars in the smallest possible number of moves, and the
Cookie Monster Problem is to determine this number for any given set of cookie jars.

Concerning data, we need a list of quantities in jars as e.g., [1, 2, 4, 12, 13, 15],
meaning that there are six jars, containing 1, 2, 4, 12, 13 and 15 cookies each.

## Data
  cookies_example.json

## Model
  constraints: Element

## Execution
  python CookieMonster.py
  python CookieMonster.py -data=cookies_example.json

## Links
  - https://bitbucket.org/oscarlib/oscar/src/dev/oscar-cp-examples/src/main/scala/oscar/cp/examples/CookieMonster.scala

## Tags
  academic
"""

from pycsp3 import *

jars = data or [15, 13, 12, 4, 2, 1]

nJars, horizon = len(jars), len(jars) + 1

# x[t][i] is the quantity of cookies in the ith jar at time t
x = VarArray(size=[horizon, nJars], dom=range(max(jars) + 1))

# y[t] is the number of cookies eaten by the monster in a selection of jars at time t
y = VarArray(size=horizon, dom=range(max(jars) + 1))

# z is the first time when all jars are empty
z = Var(dom=range(horizon))

satisfy(
    # setting initial state
    x[0] == jars,

    # setting final state
    x[-1] == 0,

    # handling the action of the cookie monster at time t (to t+1)
    [
        either(
            x[t + 1][i] == x[t][i],
            x[t + 1][i] == x[t][i] - y[t]
        ) for t in range(horizon - 1) for i in range(nJars)
    ],

    # ensuring no useless intermediate inaction
    [
        If(
            y[t] == 0,
            Then=y[t + 1] == 0
        ) for t in range(horizon - 1)
    ],

    # ensuring all jars are empty at time z
    y[z] == 0
)

minimize(
    z
)

""" Comments
1) x[0] == jars 
 is equivalent to:
   [x[0][i] == jars[i] for i in range(nJars)],
2) x[-1] == 0 
 is equivalent to:
   x[-1] == [0] * nJars
 and to:
   [x[-1][i] == 0 for i in range(nJars)],
"""
