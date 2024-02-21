# Problem RectPacking

The rectangle (square) packing problem consists of squares (bowes)
to be put in an enclosing rectangle (container) without overlapping of the squares.


## Data
  perfect-001.json

## Model
  constraints: [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python RectPacking.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-85958-1_4

## Tags
  realistic

<br />

## _Alternative Models_

#### RectPacking_z.py
 - constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap)
 - tags: academic, mzn09, mzn14
