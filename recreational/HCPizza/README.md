# Problem HCPizza
## Description
A model for the Practice Problem of Google Hash Code 2017.

The pizza corresponds to a 2-dimensional grid of n rows and m columns.
Each cell of the pizza contains either mushroom or tomato.
A slice of pizza is a rectangular section of the pizza delimited by two rows and two columns, without holes.
The slices we want to cut out must contain at least L cells of each ingredient
and at most H cells of any kind in total.
The slices being cut out cannot overlap, and do not need to cover the entire pizza.
The goal is to cut correct slices out of the pizza maximizing the total number of cells in all slices.

## Data (example)
  10-10-2-6.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python HCPizza.py -data=<datafile.json>
  - python HCPizza.py -parser=HCPizza_Random.py 20 20 2 8 2 (-dataExport)
  - python HCPizza.py -data=<datafile.txt> -parser=HCPizza_Parser.py

## Links
  - https://www.academia.edu/31537057/Pizza_Practice_Problem_for_Hash_Code_2017
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  recreational, ghc, xcsp23
