"""
This is [Problem 029](https://www.csplib.org/Problems/prob029/) at CSPLib.

This problem, posed first by G.L. Honaker, is to put a queen and the n<sup>2</sup> numbers 1...,n<sup>2</sup>
on a nxn  chessboard so that:
 - no two numbers are on the same cell,
 - any number i+1 is reachable by a knight move from the cell containing i
 - the number of “free” primes (i.e., primes not attacked by the queen) is minimal.

Note that 1 is not prime, and that the queen does not attack its own cell.

## Example
  The optimum for a chessboard of size 8 is 9.

## Data
  A number n, the size of the chessboard.

## Model
  There are several variants

  constraints: AllDifferent, Sum, Table

## Execution
  python QueenAttacking.py
  python QueenAttacking.py -data=number
  python QueenAttacking.py -data=number -variant=aux
  python QueenAttacking.py -data=number -variant=hybrid
  python QueenAttacking.py -data=number -variant=table

## Links
  - https://www.csplib.org/Problems/prob029/

## Tags
  academic, csplib
"""

from pycsp3 import *

assert not variant() or variant("aux") or variant("hybrid") or variant("table")

n = data or 8

primes = all_primes(n * n)
m = len(primes)


def row(v):
    return v // n


def col(v):
    return v % n


# q is the cell for the queen
q = Var(dom=range(n * n))

# x[i] is the cell for the i+1th value
x = VarArray(size=n * n, dom=range(n * n))

if not variant():
    satisfy(
        # all values are put in different cells
        AllDifferent(x),

        # ensuring a knight move between two successive values
        [
            (d1 == 1) & (d2 == 2) | (d1 == 2) & (d2 == 1)
            for i in range(n * n - 1) if (d1 := abs(row(x[i]) - row(x[i + 1])), d2 := abs(col(x[i]) - col(x[i + 1])))
        ]
    )

    minimize(
        # minimizing the number of free primes
        Sum(
            either(
                q == x[j],
                conjunction(row(q) != row(x[j]), col(q) != col(x[j]), abs(row(q) - row(x[j])) != abs(col(q) - col(x[j])))
            ) for j in [p - 1 for p in primes]
        )
    )

elif variant("aux"):
    # p[k] is 1 iff the k+1th prime number is not attacked by a queen
    p = VarArray(size=m, dom={0, 1})

    satisfy(
        # all values are put in different cells
        AllDifferent(x),

        # ensuring a knight move between two successive values
        [
            (d1 == 1) & (d2 == 2) | (d1 == 2) & (d2 == 1)
            for i in range(n * n - 1) if (d1 := abs(row(x[i]) - row(x[i + 1])), d2 := abs(col(x[i]) - col(x[i + 1])))
        ],

        # determining if prime numbers are attacked by the queen
        [
            p[k] == either(
                q == x[j],
                Or=conjunction(row(q) != row(x[j]), col(q) != col(x[j]), abs(row(q) - row(x[j])) != abs(col(q) - col(x[j])))
            ) for k, j in enumerate(p - 1 for p in primes)
        ]
    )

    minimize(
        # minimizing the number of free primes
        Sum(p)
    )

elif variant("hybrid"):  # hybrid as compilation will build and combine both intension and extension constraints for the list of constraints about knight moves
    satisfy(
        # all values are put in different cells
        AllDifferent(x),

        # ensuring a knight move between two successive values
        [(abs(row(x[i]) - row(x[i + 1])), abs(col(x[i]) - col(x[i + 1]))) in {(1, 2), (2, 1)} for i in range(n * n - 1)]
    )

    minimize(
        # minimizing the number of free primes
        Sum((q == x[j]) | (row(q) != row(x[j])) & (col(q) != col(x[j])) & (abs(row(q) - row(x[j])) != abs(col(q) - col(x[j]))) for j in [p - 1 for p in primes])
    )

elif variant("table"):
    def neighbours(r1, c1):
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        return [(r1 + r2) * n + c1 + c2 for (r2, c2) in jumps if 0 <= r1 + r2 < n and 0 <= c1 + c2 < n]


    T1 = {(i, j) for i in range(n * n) for j in neighbours(i // n, i % n)}
    T2 = {(i, j, 1 if i == j or i // n != j // n and i % n != j % n and abs(i // n - j // n) != abs(i % n - j % n) else 0)
          for i in range(n * n) for j in range(n * n)}

    # p[j] is 1 iff the j+1th prime number is not attacked by a queen
    p = VarArray(size=m, dom={0, 1})

    satisfy(
        # all values are put in different cells
        AllDifferent(x),

        # ensuring a knight move between two successive values
        [(x[i], x[i + 1]) in T1 for i in range(n * n - 1)],

        # determining if prime numbers are attacked by the queen
        [(q, x[k], p[j]) in T2 for j, k in enumerate(p - 1 for p in primes)]
    )

    minimize(
        # minimizing the number of free primes
        Sum(p)
        # (q == x[j]) | (row(q) != row(x[j])) & (col(q) != col(x[j])) & (abs(row(q) - row(x[j])) != abs(col(q) - col(x[j]))) for j in [p - 1 for p in primes])
    )

""" Comments
1) The variant hybrid involves the automatic introduction of auxiliary variables
2)  Sum((q == x[j]) | ((row(q) != row(x[j])) & (col(q) != col(x[j])) & (abs(row(q) - row(x[j])) != abs(col(q) - col(x[j])))) for j in
            [p - 1 for p in primes])
"""
