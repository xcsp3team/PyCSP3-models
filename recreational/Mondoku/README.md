# Problem: Mondoku

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original mzn model was written by Mikael Zayenz Lagerkvist (MIT Licence).

## Data
  three integers denoting width, height and number of colors

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Precedence](https://pycsp.org/documentation/constraints/Precedence)

## Execution
```
  python Mondoku.py -data=[number,number,number]
```

## Links
  - https://www.reddit.com/r/generative/comments/1fxp5ng/irregular_mondoku_art/
  - https://www.minizinc.org/challenge2025/results2025.html

## Tags
  academic, recreational, mzn25
