# Problem: GeneralizedPeacableQueens

Generalized Peaceable Queens.

On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hendrik 'Henk' Bierlee, under the MIT Licence.

## Data
  two integers (n,q)

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Lex](https://pycsp.org/documentation/constraints/Lex), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Regular](https://pycsp.org/documentation/constraints/Regular)

## Execution
```
  python GeneralizedPeacableQueens.py -data=[number,number]
```

## Links
  - https://oeis.org/A250000
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  academic, mzn22
