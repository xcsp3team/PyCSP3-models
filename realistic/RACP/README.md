# Problem RACP
## Description
Resource Availability Cost Problem (also known as Resource Investment Problem).
See EJOR paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018/2020 Minizinc challenges.
The MZN model was proposed by Andreas Schutt.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  j30-13-6-1-25.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RACP.py -data=<datafile.json>
  python RACP.py -data=<datafile.dzn> -parser=RACP_ParserZ.py
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S037722171730927X?via%3Dihub
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn18, mzn20
