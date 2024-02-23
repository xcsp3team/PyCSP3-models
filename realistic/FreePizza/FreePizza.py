"""
Taken from the Intelligent Systems course at Simon Fraser University.

The problem arises in the University College Cork student dorms. There is a large order
of pizzas for a party, and many of the students have vouchers for acquiring discounts in purchasing
pizzas. A voucher is a pair of numbers e.g. (2, 4), which means if you pay for 2 pizzas then you can
obtain for free up to 4 pizzas as long as they each cost no more than the cheapest of the 2 pizzas you
paid for. Similarly a voucher (3, 2) means that if you pay for 3 pizzas you can get up to 2 pizzas for
free as long as they each cost no more than the cheapest of the 3 pizzas you paid for. The aim is to
obtain all the ordered pizzas for the least possible cost. Note that not all vouchers need to be used.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  pizza06.json

## Model
  constraints: Count, Sum

## Execution
  python FreePizza.py -data=<datafile.json>

## Tags
  realistic, notebook
"""

from pycsp3 import *

prices, vouchers = data
pay, free = zip(*vouchers)
nPizzas, nVouchers = len(prices), len(pay)

# v[i] is the voucher used for the ith pizza. 0 means that no voucher is used.
# A negative (resp., positive) value i means that the ith pizza contributes to the pay (resp., free) part of voucher |i|.
v = VarArray(size=nPizzas, dom=range(-nVouchers, nVouchers + 1))

# p[i] is the number of paid pizzas wrt the ith voucher
p = VarArray(size=nVouchers, dom=lambda i: {0, pay[i]})

# f[i] is the number of free pizzas wrt the ith voucher
f = VarArray(size=nVouchers, dom=lambda i: range(free[i] + 1))

satisfy(
    # counting paid pizzas
    [Count(v, value=-i - 1) == p[i] for i in range(nVouchers)],

    # counting free pizzas
    [Count(v, value=i + 1) == f[i] for i in range(nVouchers)],

    # a voucher, if used, must contribute to have at least one free pizza.
    [(f[i] == 0) == (p[i] != pay[i]) for i in range(nVouchers)],

    # a free pizza obtained with a voucher must be cheaper than any pizza paid wrt this voucher
    [
        If(
            v[i] < 0,
            Then=v[i] != -v[j]
        ) for i in range(nPizzas) for j in range(nPizzas) if prices[i] < prices[j]
    ]
)

minimize(
    # minimizing summed up costs of pizzas
    Sum((v[i] <= 0) * prices[i] for i in range(nPizzas))
)

annotate(decision=v)

""" Comments
1) do you think that [(f[i] == 0) == (p[i] != vouchers[i].payPart) for i in range(nVouchers)] is clearer?
"""
