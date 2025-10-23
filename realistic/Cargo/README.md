# Problem: Cargo

This is a real-world cargo assembly planning problem arising in a coal supply chain.
The cargoes are built on the stockyard at a port terminal from coal delivered by trains.
Then the cargoes are loaded onto vessels.
Only a limited number of arriving vessels is known in advance.
The goal is to minimize the average delay time of the vessels over a long planning period.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2017/2018 Minizinc challenges.
See links below to papers related to this problem.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  22.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Cargo.py -data=<datafile.json>
  python Cargo.py -data=<datafile.dzn> -parser=Cargo_ParserZ.py
```

## Links
  - https://optimization-online.org/wp-content/uploads/2013/02/3755.pdf
  - https://www.sciencedirect.com/science/article/pii/S2192437620301217
  - https://link.springer.com/chapter/10.1007/978-3-319-07046-9_12
  - https://www.minizinc.org/challenge/2018/results/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  realistic, mzn13, mzn17, mzn18, xcsp24
