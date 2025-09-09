# Problem: Ghoulomb

This is a variation of the classic Golomb ruler problem, proposed for Minizinc challenges:
  - three Golomb rulers are constructed, but only the second one has to be minimized
  - Cumulative is used instead of AllDifferent
  - instead of a resource with capacity 1 and tasks that use 1 capacity unit, the capacity is set to use
    more than half of the possible maximum capacity

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2013 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integer values (m1,m2,m3)

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative)

## Execution
```
  python Ghoulomb.py -data=[number,number,number]
```

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  academic, mzn10, mzn13
