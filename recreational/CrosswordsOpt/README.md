# Problem CrosswordsOpt

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  execute 'python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py -export' to get JSON files

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CrosswordsOpt.py -data=<datafile.json>
  python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  recreational, mzn17
