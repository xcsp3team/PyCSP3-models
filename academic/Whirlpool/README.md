# Problem: Whirlpool

Perfect diagonal extended whirlpool permutation

A whirlpool permutation is an n x m matrix containing number 1..n*m where every 2x2 sub matrix is either ordered cw (clockwise) or ccw (counter-clockwise).
An extended whirlpool permutation requires that the outside ring is ordered cw or ccw, and the ring inside it, etc.
A perfect diagonal whirlpool permutation required n = m and that the sum of both diagonals is n*(n+1)*(n+1) div 2.

The model, below, is close to (can be seen as the close translation of) the one submitted to the M2020 inizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  Two integers (n,m)

## Model
  Constraints: AllDifferent, Sum

## Execution
```
  python Whirlpool.py -data=[number,number]
```

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  academic, mzn20
