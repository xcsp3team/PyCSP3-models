# Problem: RectPacking

The rectangle (square) packing problem consists of squares (boxes)
to be put in an enclosing rectangle (container) without overlapping of the squares.


## Data Example
  perfect-001.json

## Model
  constraints: [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python RectPacking.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-85958-1_4

## Tags
  realistic

<br />

## _Alternative Model(s)_

#### RectPacking_z.py
 - constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap)
 - tags: academic, mzn09, mzn14
