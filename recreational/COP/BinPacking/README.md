# Problem BinPacking

## Description
A Bin Packing Problem. 

 [Bin Packing Library](https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library): 
The bin packing problem (BPP) can be informally defined in a very simple way. We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c. The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.


## Data

- binCapacity: the capacities of bins
- itemWeights (tuple): the weights of each item 

An example is provided in the json file.

## Model
There are two variants: 
 - one with extension constraints
 - one with sum and decreasing constraints.

*Involved Constraints*: [BinPacking](https://pycsp.org/documentation/constraints/BinPacking) [Cardinality](https://pycsp.org/documentation/constraints/Cardinality) [Extension](https://pycsp.org/documentation/constraints/Extension) [Sum](https://pycsp.org/documentation/constraints/Sum) [LexDecreasing](https://pycsp.org/documentation/constraints/LexDecreasing) [Decreasing](https://pycsp.org/documentation/constraints/Decreasing)


## Command Line

```shell
python3 BinPacking.py -data=BinPacking_n1c1w4a.json [-solve]
```


