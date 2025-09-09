# Problem: GraphMaxAcyclic

Given an edge-weighted directed graph with possibly many cycles, the task is to find an acyclic sub-graph of maximal weight.

## Data Example
  example.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python GraphMaxAcyclic.py -data=<datafile.json>
  python GraphMaxAcyclic.py -data=<datafile.json> -variant=cnt
  python GraphMaxAcyclic.py -data=<datafile.txt> -dataparser=GraphMaxAcyclic_Parser.py
```

## Tags
  recreational
