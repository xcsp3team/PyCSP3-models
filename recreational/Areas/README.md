# Problem: Areas

See "Teaching Constraints through Logic Puzzles" by Peter Szeredi.

A rectangular board is given with some squares specified as positive integers.
Fill in all squares of the board with positive integers so that any maximal contiguous set of squares containing the same integer
has the area equal to this integer (two squares are contiguous if they share a side).

Important: we assume in the model below that each specified integer delimits its own region
(i.e., we cannot use two equal specified integers for the same region).

## Data Example
  3-3-3.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python Areas.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24662-6_11
  - https://www.comp.nus.edu.sg/~henz/projects/puzzles/arith/index.html

## Tags
  recreational
