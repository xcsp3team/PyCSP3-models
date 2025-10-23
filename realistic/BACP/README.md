# Problem: BACP

Problem 30 in CSPLib.

BACP is to design a balanced academic curriculum by assigning periods to courses in a way that the academic load of each period is balanced,
i.e., as similar as possible.

## Data Illustration
  10.json

## Model
  There are two variants:
   - one with extension constraints
   - one with intension constraints
  and one subvariant "d"

  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python BACP.py -data=<datafile.json> -variant=m1
  python BACP.py -data=<datafile.json> -variant=m2
  python BACP.py -data=<datafile.json> -variant=m1-d
  python BACP.py -data=<datafile.json> -variant=m2-d
```

## Links
 - https://www.csplib.org/Problems/prob030/
 - https://www.researchgate.net/publication/2521521_Modelling_a_Balanced_Academic_Curriculum_Problem
 - https://webperso.info.ucl.ac.be/~pdupont/pdupont/pdf/BACP_symcon_07.pdf

## Tags
  realistic, notebook, csplib

<br />

## _Alternative Model(s)_

#### BACP_z.py
 - constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, csplib, mzn10, mzn11
