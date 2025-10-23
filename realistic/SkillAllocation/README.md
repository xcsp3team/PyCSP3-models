# Problem: SkillAllocation

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  2w-1.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SkillAllocation.py -data=<datafile.json>
  python SkillAllocation.py -data=<datafile.dzn> -parser=SkillAllocation_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn20, mzn25
