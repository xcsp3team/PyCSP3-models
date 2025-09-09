# Problem: League

Make leagues for some games:
 - ranking should be close in each league
 - in a league, variety of country (where player comes from) is needed

## Data
  010-03-04.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python League.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic

<br />

## _Alternative Model(s)_

#### League13.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn13
#### League_z.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn12
