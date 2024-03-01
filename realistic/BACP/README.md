# Problem BACP

Problem 30 of the CSPLib.

BACP is to design a balanced academic curriculum by assigning periods to courses in a way that the academic load of each period is balanced,
i.e., as similar as possible.

## Data Example
  10.json

## Model
  There are two variants:
   - one with extension constraints
   - one with intension constraints
  and one subvariant "d"

  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python BACP.py -data=<datafile.json> -variant=m1
  python BACP.py -data=<datafile.json> -variant=m2
  python BACP.py -data=<datafile.json> -variant=m1-d
  python BACP.py -data=<datafile.json> -variant=m2-d
```

## Links
 - https://www.csplib.org/Problems/prob030/

## Tags
  realistic, notebook, csplib

<br />

## _Alternative Model(s)_

#### BACP_z.py
 - constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, csplib, mzn10, mzn11
