# Problem QueenAttacking
## Description
This is the [problem 029](https://www.csplib.org/Problems/prob029/) of the CSPLib:

This problem, posed first by G.L. Honaker, is to put a queen and the n<sup>2</sup> numbers 1...,n<sup>2</sup>
on a nxn  chessboard so that:
 - no two numbers are on the same cell,
 - any number i+1 is reachable by a knight move from the cell containing i
 - the number of “free” primes (i.e., primes not attacked by the queen) is minimal.

Note that 1 is not prime, and that the queen does not attack its own cell.

### Example
The optimum for a chessboard of size 8 is 9.


## Data
A number n, the size of the chessboard.

## Model(s)

There are three variants, one with table constraints, one with auxilliary variables and a hybrid one.

  constraints: [Intension](http://pycsp.org/documentation/constraints/Intension), [Extension](http://pycsp.org/documentation/constraints/Extension), [Sum](http://pycsp.org/documentation/constraints/Sum), [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent)


## Command Line

```
```
python QueenAttacking.py
python QueenAttacking.py -data=6
python QueenAttacking.py -data=6 -variant=aux
python QueenAttacking.py -data=6 -variant=hybrid
python QueenAttacking.py -data=6 -variant=table
```
```

## Tags
 academic
