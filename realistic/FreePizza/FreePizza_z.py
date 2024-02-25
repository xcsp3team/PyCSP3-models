"""
Taken from the Intelligent Systems course at Simon Fraser University.

The problem arises in the University College Cork student dorms. There is a large order
of pizzas for a party, and many of the students have vouchers for acquiring discounts in purchasing
pizzas. A voucher is a pair of numbers e.g. (2, 4), which means if you pay for 2 pizzas then you can
obtain for free up to 4 pizzas as long as they each cost no more than the cheapest of the 2 pizzas you
paid for. Similarly, a voucher (3, 2) means that if you pay for 3 pizzas you can get up to 2 pizzas for
free as long as they each cost no more than the cheapest of the 3 pizzas you paid for. The aim is to
obtain all the ordered pizzas for the least possible cost. Note that not all vouchers need to be used.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  06.json

## Model
  constraints: Sum

## Execution
  python FreePizza_z.py -data=<datafile.json>
  python FreePizza_z.py -data=<datafile.dzn> -parser=FreePizza_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  realistic, mzn15
"""

from pycsp3 import *

prices, buy, free = data
nPizzas, nVouchers = len(prices), len(buy)

# how[i] is the voucher used for the ith pizza. 0 means that no voucher is used.
# A negative (resp., positive) value i means that the ith pizza contributes to the buy (resp., free) part of voucher |i|.
how = VarArray(size=nPizzas, dom=range(-nVouchers, nVouchers + 1))

# used[i] is 1 if the ith voucher is used
used = VarArray(size=nVouchers, dom={0, 1})

satisfy(
    # assigning right number of pizzas to buy order
    [
        (
            used[v] == (Sum(how[p] == -(v + 1) for p in range(nPizzas)) >= buy[v]),
            Sum(how[p] == -(v + 1) for p in range(nPizzas)) <= used[v] * buy[v]
        ) for v in range(nVouchers)
    ],

    # assigning not too many pizzas to free order
    [Sum(how[p] == (v + 1) for p in range(nPizzas)) <= used[v] * free[v] for v in range(nVouchers)],

    # pizzas assigned to free are cheaper than pizzas assigned to buy
    [
        If(
            how[p1] < how[p2],
            Then=how[p1] != -how[p2]
        ) for p1 in range(nPizzas) for p2 in range(nPizzas) if prices[p1] < prices[p2]
    ]
)

minimize(
    # minimizing summed up costs of pizzas
    Sum((how[i] <= 0) * prices[i] for i in range(nPizzas))
)
