# Problem Areas
## Description
See "Teaching Constraints through Logic Puzzles" by Peter Szeredi

A rectangular board is given with some squares specified as positive integers.
Fill in all squares of the board with positive integers so that any maximal contiguous set of squares containing the same integer
has the area equal to this integer (two squares are contiguous if they share a side).

Important: we assume in the model below that each specified integer delimits its own region
(i.e., we cannot use two equal specified integers for the same region).

Example of Execution:
```
  python3 Areas.py -data=Areas-3-3-3.json
