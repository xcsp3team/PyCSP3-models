"""
Optimisation of Australian capital gains tax.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
The original MZN model, written by Jason Nguyen (Monash University), is accompanied of the MIT Licence.

## Data Example
  03-h39-r05-s10-3.json

## Model
  constraints: AllDifferent, Sum, Table

## Execution
  python CapitalGainsTax.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Capital_gains_tax_in_Australia
  - https://www.minizinc.org/challenge/2025/results

## Tags
  realistic, mzn25
"""

from pycsp3 import *

stock_types, trades = data
dates, trade_types, stocks, units, prices = zip(*trades)

TRADES = (BUY, SELL) = ("Buy", "Sell")
assert all(t in TRADES for t in trade_types)
assert all(v == chr(ord("A") + i) for i, v in enumerate(stock_types))

unit_buys = [t for t in trades if t.trade == BUY for _ in range(t.units)]
unit_sells = [t for t in trades if t.trade == SELL for _ in range(t.units)]
nBuys, nSells = len(unit_buys), len(unit_sells)

sdates, sprices = [unit_sells[i].date for i in range(nSells)], [unit_sells[i].price for i in range(nSells)]

min_buy_price, max_buy_price = min(t.price for t in trades if t.trade == BUY), max(t.price for t in trades if t.trade == BUY)
min_sell_price, max_sell_price = min(t.price for t in trades if t.trade == SELL), max(t.price for t in trades if t.trade == SELL)
max_disc = max_undi = nSells * (max_sell_price - min_buy_price)
max_loss = nSells * (max_buy_price - min_sell_price)

T = [(i, t.date, t.price) for i, t in enumerate(unit_buys)]

# x[i] is the bought unit of the ith sold unit
x = VarArray(size=nSells, dom=range(nBuys))

# xd[i] is the date of the ith sold unit
xd = VarArray(size=nSells, dom=dates)

# xp[i] is the price of the ith sold unit
xp = VarArray(size=nSells, dom=prices)

# discountable gains
dgains = Var(range(max_disc + 1))

# undiscountable gains
ugains = Var(range(max_undi + 1))

# losses
losses = Var(range(max_loss + 1))

# coefficients of the objective function
coeffs = VarArray(size=3, dom=lambda i: {-1, -2} if i == 2 else {1, 2})

satisfy(
    # forbidding to sell the same unit twice
    AllDifferent(x),

    # computing dates and prices of bought units
    [(x[i], xd[i], xp[i]) in T for i in range(nSells)],

    # buying before selling
    [xd[i] < sdates[i] for i in range(nSells)],

    #  tag(symmetry-breaking)
    [
        Increasing(
            [x[i] for i in range(nSells) if (tt := unit_sells[i]) and t.date == tt.date and t.stock == tt.stock and t.price == tt.price],
            strict=True
        ) for t in trades if t.trade == SELL
    ],

    # computing gains and losses
    [
        dgains == Sum(max(0, sprices[i] - xp[i]) * (sdates[i] - xd[i] >= 12) for i in range(nSells)),
        ugains == Sum(max(0, sprices[i] - xp[i]) * (sdates[i] - xd[i] < 12) for i in range(nSells)),
        losses == Sum(max(0, xp[i] - sprices[i]) for i in range(nSells)),
    ],

    # computing coefficients of the objective function
    # coeffs == [2, 2, -2],
    If(
        ugains > losses,
        Then=coeffs == [1, 2, -2],
        Else=If(
            ugains + dgains > losses,
            Then=coeffs == [1, 1, -1],
            Else=coeffs == [2, 2, -2]
        )
    )
)

minimize(
    coeffs * [dgains, ugains, losses]  # double_capital_gains
)

""" Comments
1) introducing the variable 'double_capital_gains" generates variables with very large domains
"""

# double_capital_gains = Var(range(-2 * max_loss, max(2 * max_disc + max_undi, 2 * max_undi + max_disc) + 1))

# If(
#     undiscountable_gains > losses,
#     Then=double_capital_gains == discountable_gains + 2 * undiscountable_gains - 2 * losses,
#     Else=If(
#         losses - undiscountable_gains < discountable_gains,
#         Then=double_capital_gains == discountable_gains - (losses - undiscountable_gains),
#         Else=double_capital_gains == 2 * (discountable_gains + undiscountable_gains - losses)
#     )
# )

# The taxable capital gains x2
# double_capital_gains ==
# ift(
#     undiscountable_gains > losses,
#     discountable_gains + 2 * undiscountable_gains - 2 * losses,
#     ift(
#         losses - undiscountable_gains < discountable_gains,
#         discountable_gains - (losses - undiscountable_gains),
#         2 * (discountable_gains + undiscountable_gains - losses)
#     ))

# TODO : in ACE, SumVarCoeffeLe et GE ???
# Sum(2 * dgains, 2 * ugains, -2 * losses)  # far more efficient but incomplete of course
