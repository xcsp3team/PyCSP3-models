# Problem: MultiAgentPathFinding

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2022 Minizinc challenges.
The original MZN model was proposed by Hakan Kjellerstrand, after translating the one by Neng-Fa Zhou in Picat
- no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  g16-p20-a20.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python MultiAgenPathFinding.py -data=<datafile.json>
  python MultiAgenPathFinding.py -variant=table -data=<datafile.json>
  python MultiAgentPathFinding.py -data=<datafile.dzn> -parser=MultiAgentPathFinding_ParserZ.py
```

## Links
  - https://ieeexplore.ieee.org/document/8372050
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn17, mzn22
