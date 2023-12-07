# Problem Amaze2
## Description
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03-08.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element)

## Execution
```
  python Amaze2.py -data=<datafile.json>
  python Amaze2.py -data=<datafile.dzn> -parser=Amaze_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  recreational, mzn12