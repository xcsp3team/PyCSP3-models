# Problem: BlockModeling

Block modeling has a long history in the analysis of social networks.
The core problem is to take a graph and divide it into k clusters and interactions between those clusters described by a k × k image matrix.
See CP'19 paper whose URL is given below.

## Data
  kansas.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python BlockModeling.py -data=<datafile.json>
  python BlockModeling.py -data=[datafile.txt,number] -parser=BlockModeling_Parser.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-30048-7_38
  - https://github.com/toulbar2/toulbar2/blob/master/web/TUTORIALS/tutorialCP2020.md#block-modeling-problem
  - https://forgemia.inra.fr/thomas.schiex/cost-function-library/-/tree/master/crafted/blockmodel
  - https://github.com/toulbar2/toulbar2/blob/master/web/TUTORIALS/blockmodel.py
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
