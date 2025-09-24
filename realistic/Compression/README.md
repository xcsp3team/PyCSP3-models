# Problem: Compression

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  bin-07.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Compression.py -data=<datafile.json>
  python Compression.py -data=<datafile.json> -variant=mzn
```

## Links
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
