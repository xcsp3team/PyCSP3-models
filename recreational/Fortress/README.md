# Problem: Fortress

From LPCP contest 2022 (problem 1):
     A map comprises nxm cells, some of them marked with a positive integer D to denote a point-of-interest that requires D free-of-walls cells around them;
     more specifically, no path of length D (Manhattan distance) originating from the point-of-interest can include walls.
     All point-of-interests must be inside the perimeter of the walls, the number of walls must be minimized,
     and as a second optimization criteria we prefer to minimize the amount of cells inside the perimeter of the walls.

Important: the model, below, has not been checked to exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data Example
  03.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Fortress1.py -data=<datafile.json>
  python Fortress1.py -data=<datafile.txt> -parser=Fortress_Parser.py
```

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2022/tree/main/problem-1
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, lpcp22, xcsp25

<br />

## _Alternative Model(s)_

#### Fortress2.py
 - constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)
 - tags: recreational, lpcp22, xcsp25
