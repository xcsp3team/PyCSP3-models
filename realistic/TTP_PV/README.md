# Problem TTPPV
## Description
Traveling Tournament Problem with Predefined Venues (TTPPV).
The problem consists of finding an optimal compact single round robin schedule for a sport event.
Given a set of n teams, each team has to play against every other team exactly once.
In each round, a team plays either at home or away, however no team can play more than three consecutive times at home or away.
The sum of the traveling distance of each team has to be minimized.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
The venue of each game has already been decided.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  circ08bbal.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Regular](http://pycsp.org/documentation/constraints/Regular), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TTPPV.py -data=<datafile.json>
  python TTPPV.py -data=<datafile.dzn> -parser=TTPPV_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob068/models/
  - https://link.springer.com/article/10.1007/s10951-008-0097-1
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  real, csplib, mzn14, mzn17, mzn22
