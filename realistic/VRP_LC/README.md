# Problem: VRP_LC

The Vehicle Routing Problem with Location Congestion (VRPLC) adds cumulative scheduling constraints
on to the standard Pickup and Delivery Problem with Time Windows (PDPTW).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Edward Lam, and described in the 2016 paper of Constraints Journal (see below).
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  09-05-10-s1.json

## Model
  constraints: [Circuit](https://pycsp.org/documentation/constraints/Circuit), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python VRP_LC.py -data=<datafile.json>
  python VRP_LC.py -data=<datafile.dzn> -parser=VRP_LC_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1007/s10601-016-9241-2
  - https://www.minizinc.org/challenge/2023/results/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  realistic, mzn18, mzn23, xcsp24
