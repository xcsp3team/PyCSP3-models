# Problem ProteinDesign
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2018 Minizinc challenges.
The MZN model was proposed by Simon de Givry.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  execute 'python ProteinDesign.py -data=<datafile.dzn> -parser=ProteinDesign_ParserZ.py -export' to get a JSON file

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python ProteinDesign.py -data=<datafile.json>
  python ProteinDesign.py -data=<datafile.dzn> -parser=ProteinDesign_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, mzn13, mzn18
