# Problem: Fastfood

## Data Example
  ff01.json

## Model
  constraints: [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Fastfood.py -data=<datafile.json>
  python Fastfood.py -data=<datafile.json> -variant=table
  python Fastfood.py -data=<datafile.dzn> -parser=Fastfood_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic

<br />

## _Alternative Model(s)_

#### Fastfood_z.py
 - constraints: [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn11, mzn12
