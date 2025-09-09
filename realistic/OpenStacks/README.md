# Problem: OpenStacks


## Data Example
  pb-20-20-1.json

## Model
  There are two variants of this model.

  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python OpenStacks.py -data=<datafile.json> -variant=m1
  python OpenStacks.py -data=<datafile.json> -variant=m2
```

## Links
  - https://ipg.host.cs.st-andrews.ac.uk/challenge/

## Tags
  realistic, notebook

<br />

## _Alternative Model(s)_

#### OpenStacks_z.py
 - constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn09, mzn11, mzn15
