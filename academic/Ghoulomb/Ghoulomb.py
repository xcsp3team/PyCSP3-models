"""
This is a variation of the classic Golomb ruler problem, proposed for Minizinc challenges:
  - three Golomb rulers are constructed, but only the second one has to be minimized
  - Cumulative is used instead of AllDifferent
  - instead of a resource with capacity 1 and tasks that use 1 capacity unit, the capacity is set to use
    more than half of the possible maximum capacity

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2013 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integer values (m1,m2,m3)

## Model
  constraints: Cumulative

## Execution
  python Ghoulomb.py -data=[number,number,number]

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  academic, mzn10, mzn13
"""

from pycsp3 import *

m1, m2, m3 = data
k = 0  # just used for the comments


def ruler(m):
    global k  # using a parameter of the function to be used in the comment (see 'k') is not working; this is why we need the global k
    k += 1

    # x'k'[i] is the location of the ith mark in the ruler 'k'
    x = VarArray(size=m, dom=range(m * m + 1), id="x" + str(k))

    # d'k'[k] is the distance between the two marks involved in the kth pair of marks of the ruler 'k'
    d = VarArray(size=(m * (m - 1)) // 2, dom=range(m * m + 1), id="d" + str(k))

    satisfy(
        # ensuring constraints for the ruler 'k'
        [
            [d[k] == x[j] - x[i] for k, (i, j) in enumerate(combinations(m, 2))],

            x[0] == 0,

            Increasing(x, strict=True),

            Cumulative(
                origins=d,
                lengths=1,
                heights=11)
            <= 15,

            # tag(symmetry-breaking)
            d[0] < d[-1]
        ]
    )


ruler(m1)
ruler(m2)
ruler(m3)

minimize(
    var("x2")[-1]
)

""" Comments
1) For being able to use k in the comment, k needs to be global (not directly a parameter)

2) In 2010 model is similar to the 2013 model up to a few annotations for output

3) Data are:
 (3,10,20) (3,7,20) (3,8,20) (3,9,16) (4,10,16) (4,7,16) (4,8,16) (4,9,10) (4,9,14) (4,9,18) for 2010
 (3,9,16) (3,11,29) (4,9,10) (4,9,20) (5,7,22) for 2013
 
4) Note that we can get access anywhere to the variable arrays with:
 x, d = var("x" + str(k)), var("d" + str(k))  
"""
