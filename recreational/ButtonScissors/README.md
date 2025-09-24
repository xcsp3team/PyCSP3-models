# Problem: ButtonScissors

From LPCP contest 2021 (Problem 2):
    There is a supply of buttons attached to patches, and we have to cut them out in order to complete some very expensive suits.
    Buttons in the same patch are also of mixed color, and therefore they must be properly separated after detaching.
    We have to detach buttons of the same color with a cut on cardinal directions or along diagonals.
    A cut must involve at least two buttons, and all buttons along the cut are detached, so they must have the same color.
    Given a patch with buttons, find a sequence of cuts that detaches all buttons.

## Data Example
  01.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Maximum](https://pycsp.org/documentation/constraints/Maximum)

## Execution
```
  python ButtonScissors.py -data=<datafile.json>
  python ButtonScissors.py -data=<datafile.txt> -parser=ButtonsScissors_Parser.py
```

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2021/tree/main/problem-2
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, lpcp21, xcsp25
