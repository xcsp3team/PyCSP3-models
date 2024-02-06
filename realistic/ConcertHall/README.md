# Problem ConcertHall

The concert hall scheduling problem considers a set of identical halls,
and a set of concerts each having a start time, end time and profit.
Each concert may either be allocated to a hall, or not scheduled.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Graeme Gange.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  002.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Precedence](http://pycsp.org/documentation/constraints/Precedence), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python ConcertHall.py -data=<datafile.json>
  python ConcertHall.py -data=<datafile.dzn> -parser=ConcertHall_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1007/s10601-006-7095-8
  - https://link.springer.com/chapter/10.1007/978-3-319-98334-9_10
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, mzn18
