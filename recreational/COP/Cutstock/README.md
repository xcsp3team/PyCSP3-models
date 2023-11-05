# Problem Cutstock
## Description

Related papers:
 - "*Mathematical methods of organizing and planning production*", L. V. Kantorovich, Management Science, 6(4):366–422, 1960
 - "*From High-Level Model to Branch-and-Price Solution in G12*", J. Puchinger, P. Stuckey, M. Wallace, and S. Brand, CPAIOR 2008: 218-232

## Data
 - nPieces, pieceLengths: the number and the sizes of pieces
 - items (tuple): each item has a length and a demand.

An example is given in the json file.

## Model
  constraints: [Decreasing](http://pycsp.org/documentation/constraints/Decreasing), [LexDecreasing](http://pycsp.org/documentation/constraints/LexDecreasing), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Command Line
```
python Cutstock.py -data=Cutstock_small.json
