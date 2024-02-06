# Problem GraphMaxAcyclic

Given a edge-weighted directed graph with possibly many cycles, the task is to find an acyclic sub-graph of maximal weight.

## Data Example
  example.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python GraphMaxAcyclic.py -data=<datafile.json>
  python GraphMaxAcyclic.py -data=<datafile.json> -variant=cnt
  python GraphMaxAcyclic.py -data=<datafile.txt> -dataparser=GraphMaxAcyclic_Parser.py
```


## Tags
  recreational
