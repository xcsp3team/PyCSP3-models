# Problem: TTP_PV

Traveling Tournament Problem with Predefined Venues (TTPPV).
The problem consists of finding an optimal compact single round-robin schedule for a sport event.
Given a set of n teams, each team has to play against every other team exactly once.
In each round, a team plays either at home or away, however no team can play more than three consecutive times at home or away.
The sum of the traveling distance of each team has to be minimized.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
The venue of each game has already been decided.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  circ08bbal.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TTP_PV.py -data=<datafile.json>
  python TTP_PV.py -data=<datafile.dzn> -parser=TTP_PV_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob068/models/
  - https://link.springer.com/article/10.1007/s10951-008-0097-1
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, csplib, mzn14, mzn17, mzn22
