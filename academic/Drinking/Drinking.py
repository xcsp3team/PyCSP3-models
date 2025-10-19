"""
From Marriott & Stuckey "Programming with Constraints", exercise page 184, drinking game:
"In the drinking game, one must drink one glass everytime a number is reached which is divisible by 7 or divisible by 5,
unless the previous drink was taken less than 8 numbers ago."

The model, below, correspond to an optimization variant of this problem, used for the 2024 competition.

## Data
  a number n

## Model
  constraints: Sum, Table

## Execution
  python Drinking.py -data=number

## Links
  - https://www.hakank.org/common_cp_models/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, xcsp24
"""

from pycsp3 import *

assert not variant() or variant("mini")

n = data or 101  # number of minutes (time slots)

# x[i] is 1 iff time i is drinking time
x = VarArray(size=n, dom={0, 1})

# y[i] is the  number of drinking times the 8 last minutes before time i
y = VarArray(size=n, dom=range(9))  # checks the last 8 minutesX

satisfy(
    # computing the number of drinking times every 8 minutes
    y[t] == Sum(x[max(t - 8, 0):max(t, 1)]) for t in range(1, n) if t % 5 == 0 or t % 7 == 0
)

if not variant():
    satisfy(
        # must drink when the time is divisible with 5 or 7 and there was no drinking the last 8 minutes
        [(y[t] == 0) == (x[t] == 1) for t in range(1, n) if t % 5 == 0 or t % 7 == 0]
    )

elif variant("mini"):
    satisfy(
        # must drink when the time is divisible with 5 or 7 and there was no drinking the last 8 minutes
        [(y[t], x[t]) in [(0, 1)] + [(v, 0) for v in range(1, 9)] for t in range(1, n) if t % 5 == 0 or t % 7 == 0]
    )

minimize(
    Sum(x)
)

""" Comments
1) For the competition 2024, "if t % 5 == 0 or t % 7 == 0" was not present Line 20
2) Linear Relaxation allows us to find optimality  
3) Data used for the 2024 competition are: [50, 100, 200, 400, 700, 10000, 20000, 50000, 100000, 200000]
"""
