# Problem: Subisomorphism

An instance of the subgraph isomorphism problem is defined by a pattern graph Gp = (Vp, Ep) and a target graph Gt = (Vt, Et):
the objective is to determine whether Gp is isomorphic to some subgraph(s) in Gt.

## Data Example
  A-01.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution:
```
  python Subisomorphism.py -data=<datafile.json>
  python Subisomorphism.py -parser=Subisomorphism_Parser.py -data=[filename1,filename2]
```

## Links
  - https://www.sciencedirect.com/science/article/pii/S0004370210000718
   - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  recreational, notebook, xcsp24
