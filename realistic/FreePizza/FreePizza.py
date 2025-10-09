"""
Taken from the Intelligent Systems course at Simon Fraser University.

The problem arises in the University College Cork student dorms. There is a large order
of pizzas for a party, and many of the students have vouchers for acquiring discounts in purchasing
pizzas. A voucher is a pair of numbers e.g. (2, 4), which means if you pay for 2 pizzas then you can
obtain for free up to 4 pizzas as long as they each cost no more than the cheapest of the 2 pizzas you
paid for. Similarly, a voucher (3, 2) means that if you pay for 3 pizzas you can get up to 2 pizzas for
free as long as they each cost no more than the cheapest of the 3 pizzas you paid for. The aim is to
obtain all the ordered pizzas for the least possible cost. Note that not all vouchers need to be used.

## Data Example
  06b.json

## Model
  constraints: Count, Sum

## Execution
  python FreePizza.py -data=<datafile.json>

## Tags
  realistic, notebook
"""

from pycsp3 import *

prices, vouchers = data or load_json_data("06b.json")

nPizzas, nVouchers = len(prices), len(vouchers)
P, V = range(nPizzas), range(nVouchers)

# x[p] is the voucher used for pizza p. 0 means that no voucher is used.
# A negative (resp., positive) value v means that pizza p contributes to the pay (resp., free) part of voucher |v|.
x = VarArray(size=nPizzas, dom=range(-nVouchers, nVouchers + 1))

# pp[v] is the number of paid pizzas wrt voucher v
pp = VarArray(size=nVouchers, dom=lambda i: {0, vouchers[i].pay})

# fp[v] is the number of free pizzas wrt voucher v
fp = VarArray(size=nVouchers, dom=lambda i: range(vouchers[i].free + 1))

satisfy(
    # counting paid pizzas
    [
        Count(
            within=x,
            value=-v - 1
        ) == pp[v] for v in V
    ],

    # counting free pizzas
    [
        Count(
            within=x,
            value=v + 1
        ) == fp[v] for v in V
    ],

    # a voucher, if used, must contribute to have at least one free pizza.
    [
        (fp[v] == 0) == (pp[v] != vouchers[v].pay)
        for v in V
    ],

    # a free pizza obtained with a voucher must be cheaper than any pizza paid wrt this voucher
    [
        If(
            x[p1] < 0,
            Then=x[p1] != -x[p2]
        ) for p1 in P for p2 in P if prices[p1] < prices[p2]
    ]
)

minimize(
    # minimizing summed up costs of pizzas
    Sum((x[p] <= 0) * prices[p] for p in P)
)

annotate(decision=x)
