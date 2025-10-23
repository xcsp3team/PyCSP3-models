# Problem: CrosswordsOpt

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  execute 'python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py -export' to get JSON files

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CrosswordsOpt.py -data=<datafile.json>
  python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2017/results/

## Tags
  recreational, mzn17
