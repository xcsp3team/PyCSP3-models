"""
Block modeling has a long history in the analysis of social networks.
The core problem is to take a graph and divide it into k clusters and interactions between those clusters described by a k × k image matrix.
See CP'19 paper whose URL is given below.

## Data Illustration
  kansas.json

## Model
  constraints: Sum

## Execution
  python BlockModeling.py -data=<datafile.json>
  python BlockModeling.py -data=[datafile.txt,number] -parser=BlockModeling_Parser.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-30048-7_38
  - https://github.com/toulbar2/toulbar2/blob/master/web/TUTORIALS/tutorialCP2020.md#block-modeling-problem
  - https://forgemia.inra.fr/thomas.schiex/cost-function-library/-/tree/master/crafted/blockmodel
  - https://github.com/toulbar2/toulbar2/blob/master/web/TUTORIALS/blockmodel.py
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

matrix, nBlocks = data or load_json_data("kansas-2.json")

nNodes = len(matrix)
N, B = range(nNodes), range(nBlocks)

# x[i][j] is the value in the grid at the ith row and jth column
x = VarArray(size=[nBlocks, nBlocks], dom={0, 1})

# y[k] is the block index of the kth node
y = VarArray(size=nNodes, dom=range(nBlocks))

satisfy(
    # partial symmetry breaking constraint
    y[u] <= u for u in B[:-1]
)

minimize(
    Sum(
        conjunction(
            y[i] == u,
            y[j] == v,
            x[u][v] != matrix[i][j]
        ) for u in B for v in B for i in N for j in N if i != j
    )
    + Sum(
        both(
            y[i] == u,
            x[u][u] != matrix[i][i]
        ) for u in B for i in N
    )
)
