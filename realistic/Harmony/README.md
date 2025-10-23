# Problem: Harmony

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  brother.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Harmony.py -data=<datafile.json>
  python Harmony.py -data=<datafile.dzn> -parser=Harmony_ParserZ.py
```

## Links
  - https://www.ijcai.org/proceedings/2024/858
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
