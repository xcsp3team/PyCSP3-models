# Problem OpenStacks


## Data Example
  pb-20-20-1.json

## Model
  There are two variants of this model.

  constraints: [Alldifferent](http://pycsp.org/documentation/constraints/Alldifferent), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python OpenStacks.py -data=<datafile.json> -variant=m1
  python OpenStacks.py -data=<datafile.json> -variant=m2
```

## Links
  - https://ipg.host.cs.st-andrews.ac.uk/challenge/

## Tags
  realistic

<br />

## _Alternative Models_

#### OpenStacks_z.py
 - constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn09, mzn11, mzn15
