# Problem OPD

An OPD (v,b,r) problem is to find a binary matrix of v rows and b columns such that:
   - each row sums to r,
   - the dot product between any pair of distinct rows is minimal

## Data
  Three integers (v,b,r)

## Model
  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python OPD.py -data=[number,number,number]
  python OPD.py -data=[number,number,number] -variant=aux
```

## Links
  - https://www.csplib.org/Problems/prob065/
  - https://link.springer.com/article/10.1007/s10601-006-9014-4
  - https://www.sciencedirect.com/science/article/abs/pii/S1571065314000596?via%3Dihub
  - https://link.springer.com/chapter/10.1007/11564751_7
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  academic, csplib

<br />

## _Alternative Models_

#### OPD_z.py
 - constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: academic, csplib, mzn15, mzn17
