# Problem RadarSurveillance

This is a Radar surveillance instance where some radars must be put on a geographic area of a specified size and must cover all cells.
There are some insignificant cells that must not be covered by any radar. All other cells must be covered by exactly a specified number of radars.
Instances of this problem follow the description given by the Swedish Institute of Computer Science (SICS).

## Data
  8-24-3-2-00.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python RadarSurveillance.py -data=<datafile.json>
```

## Links
 - https://en.wikipedia.org/wiki/Magic_square

## Tags
  realistic
