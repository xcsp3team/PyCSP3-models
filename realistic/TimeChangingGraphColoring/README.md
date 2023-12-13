# Problem TimeChangingGraphColoring
## Description
Time-changing Graph Coloring Problem.

The problem is to minimize the number of steps for converting an initial coloring to an end coloring
by applying at most "k" changes of colors at each step, while always maintaining a valid coloring.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  k05-05.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TimeChangingGraphColoring.py -data=<datafile.json>
  python TimeChangingGraphColoring.py -data=<datafile.dzn> -parser=TimeChangingGraphColoring_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn17
