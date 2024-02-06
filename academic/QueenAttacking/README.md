# Problem QueenAttacking

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

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python QueenAttacking.py
  - python QueenAttacking.py -data=number
  - python QueenAttacking.py -data=number -variant=aux
  - python QueenAttacking.py -data=number -variant=hybrid
  - python QueenAttacking.py -data=number -variant=table

## Tags
  academic, csplib
