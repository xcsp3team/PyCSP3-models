# Problem: PeacableQueens

On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The model was created by Hendrik 'Henk' Bierlee, with a licence that seems to be like a MIT Licence.

## Data
  An integer n

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Lex](https://pycsp.org/documentation/constraints/Lex), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Regular](https://pycsp.org/documentation/constraints/Regular)

## Execution
```
  python PeacableQueens.py -data=number
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://oeis.org/A250000
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
