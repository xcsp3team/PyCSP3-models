# Problem GBACP

This is a generalisation of the Balanced Academic Curriculum Problem (BACP) proposed by
Marco Chiarandini, Luca Di Gaspero, Stefano Gualandi, and Andrea Schaerf at University of Udine.
See CSPLib.

## Data
  UD04.json

## Model
  Two variants compute differently the delta values:
  - a main variant involving the constraint Maximum
  - a variant 'table' involving binary table constraints

  constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python GBACP.py -data=<datafile.json>
  - python GBACP.py -data=<datafile.json> -variant=table

## Links
  - https://opthub.uniud.it/problem/timetabling/gbac
  - https://link.springer.com/chapter/10.1007/978-3-540-88439-2_11
  - https://www.csplib.org/Problems/prob064/
  - https://www.minizinc.org/challenge2020/results2020.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, csplib, mzn16, mzn17, mzn20, xcsp23

<br />

## _Alternative Model(s)_

#### GBACP_z.py
 - constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, csplib, mzn16, mzn17, mzn20
