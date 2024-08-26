"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The original model was written by Kelvin Davis (MIT Licence).

## Data Example
  nl07-m10-134.json

## Model
  constraints: AllDifferent, Count, Element, Sum

## Execution
  python Gametes.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

maxCrossovers, nLoci, nGametes, nTreeCells, gametes = data

Node, Leaf, Null = NodeType = range(3)

treeType = VarArray(size=nTreeCells, dom=NodeType)

treeLeft = VarArray(size=nTreeCells, dom=range(-1, nTreeCells))

treeRight = VarArray(size=nTreeCells, dom=range(-1, nTreeCells))

xs = VarArray(size=[nTreeCells, nLoci], dom={0, 1})

index = VarArray(size=nTreeCells, dom=range(-1, nGametes))

source = VarArray(size=[nTreeCells, nLoci], dom={1, 2})

swap = VarArray(size=[nTreeCells, nLoci], dom=lambda i, j: {0, 1} if j > 0 else None)

satisfy(

    # Tree structure
    Increasing(treeType),

    [
        If(
            treeType[i] == Node,
            Then=[
                treeLeft[i] > i,
                treeRight[i] > i,
                treeType[treeLeft[i]] != Null,
                treeType[treeRight[i]] != Null],
            Else=[
                treeLeft[i] == -1,
                treeRight[i] == -1]
        ) for i in range(nTreeCells)
    ],

    [
        (
            (treeType[i] == Leaf) == (index[i] != -1),
            (treeType[i] == Null) == (xs[i] == 0)
        ) for i in range(nTreeCells)
    ],

    AllDifferent(index, excepting=-1),

    [
        If(
            treeType[i] == Leaf,
            Then=[xs[i][j] == gametes[index[i], j] for j in range(nLoci)]
        ) for i in range(nTreeCells)
    ],

    # First plant is the desired plant
    [
        xs[0] == 1,
        treeType[0] != Null
    ],

    # Each internal node and its child nodes (genetic parents in reality) must be related by crossing
    [
        If(
            treeType[i] == Node,
            Then=[
                [swap[i][j] == (source[i][j - 1] != source[i][j]) for j in range(1, nLoci)],
                Sum(swap[i]) <= maxCrossovers,
                [xs[i][j] == ift(source[i][j] == 1, xs[treeLeft[i], j], xs[treeRight[i], j]) for j in range(nLoci)]
            ],
            Else=[
                [source[i][j] == 1 for j in range(nLoci)],
                [swap[i][j] == 0 for j in range(1, nLoci)]
            ]
        ) for i in range(nTreeCells)
    ],

    # tag(symmetry-breaking)
    [
        If(
            treeType[i] == Node,
            Then=[
                Exist(xs[i, j] > xs[treeRight[i], j] for j in range(nLoci)),
                Exist(xs[i, j] > xs[treeLeft[i], j] for j in range(nLoci)),
                Exist(xs[treeLeft[i], j] > xs[treeRight[i], j] for j in range(nLoci)),
                Exist(xs[treeRight[i], j] > xs[treeLeft[i], j] for j in range(nLoci))
            ]
        ) for i in range(nTreeCells)
    ]
    ,
)

minimize(
    Sum(treeType[i] == Node for i in range(nTreeCells))
    # Count(treeType, value=Node)
)

""" Comments
1) Symmetry-breaking constraint are very long to generate. What to do?
"""
