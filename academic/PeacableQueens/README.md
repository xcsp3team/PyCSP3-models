# Problem PeacableQueens
## Description
On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The model was created by Hendrik 'Henk' Bierlee, with a licence that seems to be like a MIT Licence.

## Data
  an integer n

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Lex](http://pycsp.org/documentation/constraints/Lex), [Precedence](http://pycsp.org/documentation/constraints/Precedence), [Regular](http://pycsp.org/documentation/constraints/Regular)

## Execution
```
  python PeacableQueens.py -data=[integer]
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://oeis.org/A250000
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
