# Problem Solbat
## Description
Solitaire Battleships
A puzzle where we are given a partially filled-in board and the number of ships in each row and column and have to fill it with ships.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Peter Stuckey.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  12-12-5-1.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Solbat.py -data=<datafile.json>
  python Solbat.py -data=<datafile.dzn> -parser=Solbat_ParserZ.py
```

## Links
  - http://www.csee.umbc.edu/courses/671/fall09/resources/smith06.pdf
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  recreational, mzn10, mzn11, mzn12, mzn14, mzn16
