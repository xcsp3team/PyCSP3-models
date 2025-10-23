# Problem: ProteinDesign

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2018 Minizinc challenges.
The original MZN model was proposed by Simon de Givry - no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  execute 'python ProteinDesign.py -data=<datafile.dzn> -parser=ProteinDesign_ParserZ.py -export' to get a JSON file

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python ProteinDesign.py -data=<datafile.json>
  python ProteinDesign.py -data=<datafile.dzn> -parser=ProteinDesign_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2018/results/

## Tags
  realistic, mzn13, mzn18, mzn25
