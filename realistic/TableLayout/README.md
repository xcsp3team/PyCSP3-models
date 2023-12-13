# Problem TableLayout
## Description
Automatic layout of tables is useful in word processing applications.
When the table contains text, minimizing the height of the table for a fixed maximum width is a difficult combinatorial optimization problem.
See links to papers below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  1000-1615-479.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python TableLayout.py -data=<datafile.json>
  python TableLayout.py -data=<datafile.dzn> -parser=TableLayout_ParserZ.py
```

## Links
  - https://dl.acm.org/doi/abs/10.1145/2034691.2034697
  - https://pubsonline.informs.org/doi/10.1287/ijoc.2014.0637
  - https://www.minizinc.org/challenge2011/results2011.html

## Tags
  realistic, mzn11
