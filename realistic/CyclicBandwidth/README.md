# Problem: CyclicBandwidth

## Data Example
  caterpillar13.json

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python CyclicBandwidth.py -data=<datafile.json>
  python CyclicBandwidth.py -data=<datafile.json> -variant=aux
  python CyclicBandwidth.py -data=<datafile.json> -variant=table
  python CyclicBandwidth.py -data=<datafile.txt> -parser=CyclicBandwith_Parser.py
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054814003177
  - https://www.tamps.cinvestav.mx/~ertello/cbmp.php
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
