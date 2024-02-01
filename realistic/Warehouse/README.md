# Problem Warehouse

See Problem 034 on CSPLib.

In the Warehouse Location problem (WLP), a company considers opening warehouses at some candidate locations in order to supply its existing stores.

## Data Example
  opl-example.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python Warehouse.py -data=<datafile.json>
  - python Warehouse.py -data=<datafile.json> -variant=compact
  - python Warehouse.py -data=<datafile.txt> -parser=Warehouse_Parser.py
  - python Warehouse.py -parser=Warehouse_Random.py 20 50 100 10 1000 0

## Links
  - https://www.csplib.org/Problems/prob034/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
