# Problem MultiAgentPathFinding

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2022 Minizinc challenges.
The MZN model was proposed by Hakan Kjellerstrand, after translating the one by Neng-Fa Zhou in Picat.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  g16-p20-a20.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python MultiAgenPathFinding.py -data=<datafile.json>
  python MultiAgenPathFinding.py -variant=table -data=<datafile.json>
  python MultiAgentPathFinding.py -data=<datafile.dzn> -parser=MultiAgentPathFinding_ParserZ.py
```

## Links
  - https://ieeexplore.ieee.org/document/8372050
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn17, mzn22
