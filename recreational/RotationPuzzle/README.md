# Problem RotationPuzzle

See http://www-groups.dcs.st-and.ac.uk/~gap/ForumArchive/Harris.1/Bob.1/Re__GAP_.59/1.html

This problem was called "rotation" at Nokia's web site.

The puzzle is a 4x4 grid of numbers. There are four operations, each of
which involves rotating the numbers in a 3x3 subgrid clockwise.
Given an arbitrary initial state, with all values from 0 to 15 put
in the grid, one must reach the following final state:
  ```
  0  1  2  3
  4  5  6  7
  8  9 10  11
  12 13 14 15
  ```

by applying a minimal sequence of rotations. We can observe that the effect
of rotations on the final state is given by the following cycles:
  - (0, 1, 2, 6, 10, 9, 8, 4)
  - (1, 2, 3, 7, 11, 10, 9, 5)
  - (4, 5, 6, 10, 14, 13, 12, 8)
  - (5, 6, 7, 11, 15, 14, 13, 9)

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python RotationPuzzle.py -data=number
  python RotationPuzzle.py -data=<datafile.json>
```

## Links
  - https://www.csplib.org/Problems/prob013/

## Tags
  recreational
