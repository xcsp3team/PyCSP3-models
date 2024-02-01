# Problem CollectiveConstruction

Multi-agent Collective Construction (MACC).

The multi-agent collective construction problem tasks agents to construct any given three-dimensional structure on a grid by repositioning blocks.
Agents are required to also use the blocks to build ramps in order to access the higher levels necessary to construct the building,
and then remove the ramps upon completion of the building.
See CP paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Edward Lam.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  037.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CollectiveConstruction.py -data=<datafile.json>
  python CollectiveConstruction.py -data=<datafile.dzn> -parser=CollectiveConstruction_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-58475-7_43
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
