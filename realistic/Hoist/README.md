# Problem Hoist
## Description
Hoist Scheduling (M hoists, 1 track).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by M. Wallace and N. Yorke-Smith,
and released under CC BY-NC-SA license (https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Data Example
  PU-1-2-2.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Hoist.py -data=<datafile.json>
  python Hoist.py -data=<datafile.dzn> -parser=Hoist_ParserZ.py
```

## Links
  - https://data.4tu.nl/articles/_/12682700/1
  - https://link.springer.com/article/10.1007/s10601-020-09316-z
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
