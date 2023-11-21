# Problem Pennies
## Description
Put n pennies on a chessboard, so that all distances between pennies are distinct.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.
The original model involves an option type while we use the special value -1.

## Data
  an integer n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Pennies.py -data=<number>
```

## Links
  - https://blog.computationalcomplexity.org/2023/06/can-you-put-n-pennies-on-n-x-n.html
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  academic, mzn23
