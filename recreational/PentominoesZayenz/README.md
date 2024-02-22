# Problem PentominoesZayenz

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, with a MIT Licence.

## Data Example
  s05-t20-s17-close.json

## Model
  The automatas may be non-deterministic. This is why we have two variants:
    - a main one
    - a variant called "det"

  constraints: [Regular](http://pycsp.org/documentation/constraints/Regular)

## Execution
```
  python PentominoesZayenz.py -data=<datafile.json>
  python PentominoesZayenz.py -data=<datafile.dzn> -dataparser=PentominoesZayenz_ParserZ.py
```

## Links
  - https://www.researchgate.net/publication/228523019_Modeling_irregular_shape_placement_problems_with_regular_constraints
  - https://github.com/zayenz/minizinc-pentominoes-generator
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn21
