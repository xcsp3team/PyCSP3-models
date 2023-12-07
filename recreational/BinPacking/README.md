# Problem BinPacking
## Description
A Bin Packing Problem (def from link provided below): <br />

The bin packing problem (BPP) can be informally defined in a very simple way. We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c. The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.


## Data
- binCapacity: the capacities of bins
- itemWeights (tuple): the weights of each item

An example is provided in the json file.

## Model
There are two variants:
 - one with extension constraints
 - one with sum and decreasing constraints.

  constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Decreasing](http://pycsp.org/documentation/constraints/Decreasing), [LexDecreasing](http://pycsp.org/documentation/constraints/LexDecreasing), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)


## Command Line
```
python BinPacking.py -data=BinPacking_n1c1w4a.json
```

## Links
 - https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library

## Tags
 recreational