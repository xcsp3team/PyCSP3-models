# Problem: Rehearsal

Problem 039 on CSPLib.

A concert is to consist of nine pieces of music of different durations each involving a different combination of the five members of the orchestra.

## Data Example
  rs.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Rehearsal.py -data=<datafile.json>
  python Rehearsal.py -data=<datafile.json> -variant=bis
```

## Links
  - https://www.csplib.org/Problems/prob039/

## Tags
  realistic, csplib
