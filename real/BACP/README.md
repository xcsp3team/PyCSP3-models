# Problem BACP
## Description
Balanced academic curriculum problem:
  - a curriculum is a set of courses with prerequisites
  - each course must be assigned within a set number of periods
  - a course cannot be scheduled before its prerequisites
  - each course confers a number of academic credits (its 'load')
  - students have lower and upper bounds on the number of credits they can study for in a given period
  - students have lower and upper bounds on the number of courses they can study for in a given period

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  01.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python BACP.py -data=<datafile.json>
  python BACP.py -data=<datafile.dzn> -parser=BACP_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob030/
  - https://www.minizinc.org/challenge2011/results2011.html

## Tags
  real, csplib, mzn10, mzn11
