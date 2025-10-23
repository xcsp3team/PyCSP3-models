# Problem: Stripboard

Layout for electrical components on stripboard.

Taking component footprints, pin locations and pinlist as input and trying to produce the most compact layout.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019/2022 Minizinc challenges.
MIT Licence (Copyright 2022 Monash University, model by Jason Nguyen, for the original MZN model)

## Data Example
  common-emitter-simple.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python3 Stripboard.py -data=<datafile.dzn> -parser=Stripboard_ParserZ.py
  python Stripboard.py -data=<datafile.json> -parser=Stripboard_Converter.py
  python Stripboard.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn22, mzn25
