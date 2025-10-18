"""
From Peter Szeredi (see paper cited below):
In this puzzle, a square board of n ∗ n cells is given.
The task is to place integer numbers, chosen from the range 1..m (we have m ≤ n), on certain cells of the board, so that the following conditions hold:
  - in each row and each column all integers in 1..m occur exactly once, and there are n − m empty cells;
  - along the spiral starting from the top left corner, the integers follow the pattern 1, 2, ..., m, 1, 2, ... , m, ... (number m is called the period of the spiral).
Initially, some numbers may be already placed on the board.

## Data
  Two integers n and m.

## Model
  constraints: Cardinality

## Execution
  python Spiral.py
  python Spiral.py -data=[number,number]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24662-6_11

## Tags
  academic, recreational
"""

from pycsp3 import *

assert not variant() or variant("table")

n, m = data or (7, 4)
assert n == 7 and 0 < m <= n  # for the moment, n = 7 (until we prove that nSegments is correct; see below)

nSegments = ((n - 3) // 2) * 4  # it is correct for n = 7, but for other orders?

value_sequences = [tuple(1 + (i + j) % m for j in range(m)) for i in range(m)]


def scope(k):
    assert k > 0
    if k == 1:
        return x[0]
    if k == 2:
        return x[:, -1]
    if k == 3:
        return list(reversed(x[-1]))
    gap = k // 4 - 1
    if k % 4 == 0:
        return list(reversed(x[gap + 1:n if gap == 0 else - gap, gap]))  # top
    if k % 4 == 1:
        return x[gap + 1, gap:-1 - gap]  # right
    if k % 4 == 2:
        return x[gap + 1: -1 - gap, -2 - gap]  # down
    assert k % 4 == 3
    return list(reversed(x[-2 - gap, gap + 1:-1 - gap]))  # left


# x[i][j] is the value at row i and column j
x = VarArray(size=[n, n], dom=range(m + 1))

segment_scopes = cp_array(scope(k + 1) for k in range(nSegments))  # cp_array is required here for being able to use the constraint 'element'

satisfy(
    # putting each value on each row, and also the special value 0
    [
        Cardinality(
            within=x[i],
            occurrences={0: n - m} | {v: 1 for v in range(1, m + 1)}
        ) for i in range(n)
    ],

    # putting each value on each column, and also the special value 0
    [
        Cardinality(
            within=x[:, j],
            occurrences={0: n - m} | {v: 1 for v in range(1, m + 1)}
        ) for j in range(n)
    ],
)

if not variant():
    # p[k][q] is the position of the qth (non-zero) value of the kth segment
    p = VarArray(size=[nSegments, m], dom=lambda k, q: range(len(segment_scopes[k])))

    # v[k][q] is the qth (non-zero) value of the kth segment
    v = VarArray(size=[nSegments, m], dom=range(1, m + 1))

    satisfy(
        # positions must be ordered
        [Increasing(p[k], strict=True) for k in range(nSegments)],

        # the first segment has a fixed sequence of values
        v[0] == range(1, m + 1),

        # other segments must respect authorized sequences of values
        [v[k] in value_sequences for k in range(1, nSegments)],

        # linking variables from x, p and v by means of constraints 'element'
        [segment_scopes[k][p[k][q]] == v[k][q] for k in range(nSegments) for q in range(m)]
    )


elif variant("table"):
    def table(k):
        r = len(segment_scopes[k])
        assert m <= r
        tbl = set()
        for combination in combinations(range(r), m):
            for sequence in [tuple(range(1, m + 1))] if k == 0 else value_sequences:
                t = [0] * r
                for i in range(m):
                    t[combination[i]] = sequence[i]
                tbl.add(tuple(t))
        return tbl


    satisfy(
        # enforcing each segment to contain values in ordered sequences
        Table(
            scope=segment_scopes[k],
            supports=table(k)
        ) for k in range(nSegments)

    )
