# Problem Rlfap
## Description
See "Radio Link Frequency Assignment", by B. Cabon, S. de Givry, L. Lobjois, T. Schiex, J. Warners, Constraints An Int. J. 4(1): 79-89 (1999)
## Data
A json archive is in data directory.

## Model
There exists 3 variants of this problem depending the minimization function.
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NValues](http://pycsp.org/documentation/constraints/NValues), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python3 Rlfap.py -data=Rlfap-card-scen-04.json -variant=card
  python3 Rlfap.py -data=Rlfap-span-scen-05.json -variant=span
  python3 Rlfap.py -data=Rlfap-max-graph-05.json -variant=max
```

## Links
  - https://link.springer.com/article/10.1023/A:1009812409930

## Tags
recreational
