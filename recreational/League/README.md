# Problem League

Make leagues for some games:
 - ranking should be close in each league
 - in a league, variety of country (where player comes from) is needed

## Data
  010-03-04.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python League.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic
