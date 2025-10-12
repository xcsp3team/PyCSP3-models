"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  d03.json

## Model
  constraints: Cumulative, Maximum, Minimum, Sum

## Execution
  python StackCutstock.py -data=<datafile.json>
  python StackCutstock.py -data=<datafile.dzn> -parser=StackCutstock_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
"""

from pycsp3 import *

products, stackLimit, stockPieceSize, nCuts = data or load_json_data("d03.json")

sizes, numbers = zip(*products)
nProducts = len(products)

# x[i][j] is the number of the jth product on the ith cutting stock piece
x = VarArray(size=[nCuts, nProducts], dom=range(stockPieceSize + 1))

# z[i] is the number of copies of the ith cutting stock piece
z = VarArray(size=nCuts, dom=range(max(numbers) + 1))

# used[i] is 1 if the ith cutting stock piece is used
used = VarArray(size=nCuts, dom={0, 1})

# fst[j] is the first (index of) cutting piece used for the jth product
fst = VarArray(size=nProducts, dom=range(1, nCuts + 1))

# lst[j] is the last (index of) cutting piece used for the jth product
lst = VarArray(size=nProducts, dom=range(1, nCuts + 1))

# dur[j] is the duration (in terms of sequence of cutting pieces) for the jth product
dur = VarArray(size=nProducts, dom=range(nProducts + 1))

satisfy(
    # computing first used cutting pieces
    [
        fst[j] == Minimum(
            (i + 1) + nProducts * (1 - (x[i][j] > 0)) for i in range(nCuts)
        ) for j in range(nProducts)
    ],

    # computing last used cutting pieces
    [
        lst[j] == Maximum(
            (x[i][j] > 0) * (i + 1) for i in range(nCuts)
        ) for j in range(nProducts)
    ],

    # computing durations for each product
    [dur[j] == lst[j] - fst[j] for j in range(nProducts)],

    # cutting enough of each product
    [x[:, j] * z >= numbers[j] for j in range(nProducts)],

    # respecting the stock piece size
    [x[i] * sizes <= stockPieceSize for i in range(nCuts)],

    # respecting the maximum number of open stacks
    Cumulative(
        origins=fst,
        lengths=dur,
        heights=1
    ) <= stackLimit,

    # symmetry elimination: unused cuts are at the beginning
    (
        [x[i][j] <= used[i] * stockPieceSize for i in range(nCuts) for j in range(nProducts)],
        [z[i] <= used[i] * max(numbers) for i in range(nCuts)],
        [used[i] <= z[i] for i in range(nCuts)],
        [used[i] <= used[i + 1] for i in range(nCuts - 1)]
    )
)

minimize(
    # minimizing the overall number of copies of cutting pieces
    Sum(z)
)

""" Comments
1) Compared to the MZN model, we don't use the array patterns:
   patterns = Var(range(nCuts + 1))
   patterns == Sum(used)
"""
