# Problem: EchoSched

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data
  12-12-0-1-7.json

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python EchoSched.py -data=<datafile.json>
  python EchoSched.py -data=<datafile.dzn> -parser=EchoSched_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
