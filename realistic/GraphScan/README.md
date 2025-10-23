# Problem: GraphScan

Problem of global coverage-path planning for linear-infrastructure inspection using multiple autonomous UAVs (Autonomous unmanned aerial vehicles, or drones).
The problem is mathematically formulated as a variant of the Min–Max K-Chinese Postman Problem (MM K-CPP) with multi-weight edges.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge (directory multi-agent-graph-coverage).
The original MZN model seems to have been written by Peter Schneider-Kamp (MIT Licence assumed).

## Data
  n10-p1500-c15.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum)

## Execution
```
  python GraphScan.py -data=<datafile.json>
```

## Links
  - https://findresearcher.sdu.dk/ws/portalfiles/portal/241768335/drones_07_00563.pdf
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn23
