# Problem Nside

Road Network Maintenance Problem.

The aim is to determine which worksheets to execute on which day so that the road network is not perturbed too much.
Each worksheet is a contiguous set of daily tasks on roads: specified by a road and number of workers.
Worksheets have an importance defining how important they are to execute.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  easy-0200-50.json

## Model
  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Nside.py -data=<datafile.json>
  python Nside.py -data=<datafile.dzn> -parser=Nside_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
