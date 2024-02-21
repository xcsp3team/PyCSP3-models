# Problem CVRP

See Problem 086 on CSPLib, and VVRLib.

## Data Example
  A-n32-k5.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python CVRP.py -data=<datafile.json>

## Links
  - https://www.csplib.org/Problems/prob086/
  - http://vrp.galgos.inf.puc-rio.br/index.php/en/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22

<br />

## _Alternative Models_

#### CVRP_z.py
 - constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn15
