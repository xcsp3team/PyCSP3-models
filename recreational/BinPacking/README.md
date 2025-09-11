# Problem: BinPacking

A Bin Packing Problem.

The bin packing problem (BPP) can be informally defined in a very simple way.
We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c.
The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.

## Data Example
  n1c1w4a.json

## Model
  There are two variants:
   - one with extension constraints
   - one with sum and decreasing constraints.

  constraints: [BinPacking](https://pycsp.org/documentation/constraints/BinPacking), [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Lex](https://pycsp.org/documentation/constraints/Lex), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python BinPacking.py -data=<datafile.json>
  python BinPacking.py -data=<datafile.json> -variant=table
```

## Links
  - https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24

<br />

## _Alternative Model(s)_

#### BinPacking2.py
 - constraints: [BinPacking](https://pycsp.org/documentation/constraints/BinPacking), [NValues](https://pycsp.org/documentation/constraints/NValues)
 - tags: recreational, xcsp24
