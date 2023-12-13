# Problem League
## Description
Make leagues for some games:
 - ranking should be close in each league
 - in a league, variety of country (where player comes from) is needed

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  020-3-5.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python League.py -data=<datafile.json>
  python League.py -data=<datafile.dzn> -parser=League_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
