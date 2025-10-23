# Problem: RosterSickness

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The original MZN model was proposed by Ties Westendorp, under the MIT Licence.

## Data Example
  small-4.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RosterSickness.py -data=<datafile.json>
  python RosterSickness.py -data=<datafile.dzn> -parser=RosterSickness_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn22
