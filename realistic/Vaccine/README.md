# Problem Vaccine
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Peter J. Stuckey, under the MIT Licence.
Compared to the Minizinc model, we do not use set variables.

## Data Example
  007.json

## Model
  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Lex](http://pycsp.org/documentation/constraints/Lex), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Vaccine.py -data=sm-10-13-00.json
  python Vaccine.py -data=sm-10-13-00.dzn -dataparser=Vaccine_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
