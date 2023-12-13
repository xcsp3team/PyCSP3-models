# Problem KidneyExchange
## Description
Cardinality-constrained Multi-cycle Problem (CCMCP).

This problem appears as one of the main optimization problems modelling kidney exchange.
The problem consists of the prize-collecting assignment problem and an addition constraint stipulating that each subtour in the graph
has a maximum length K.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Edward Lam and Vicky Mak-Hau.
No Licence was explicitly mentioned (MIT Licence is assumed).


## Data Example
  3-20-025-2.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Precedence](http://pycsp.org/documentation/constraints/Precedence), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python KidneyExchange.py -data=<datafile.json>
  python KidneyExchange.py -data=<datafile.dzn> -parser=KidneyExchange_ParserZ.py
  python KidneyExchange.py -data=<datafile.txt> -parser=KidneyExchange_ParserW.py
```

## Links
  - https://en.wikipedia.org/wiki/Optimal_kidney_exchange
  - https://www.preflib.org/dataset/00036
  - https://link.springer.com/article/10.1007/s10878-015-9932-4
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
