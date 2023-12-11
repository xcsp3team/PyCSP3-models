# Problem StableGoods
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  s-d06.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python StableGoods.py -data=<datafile.json>
  python StableGoods.py -data=<datafile.dzn> -parser=StableGoods_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
