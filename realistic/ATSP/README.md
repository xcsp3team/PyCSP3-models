# Problem ATSP
## Description
Artificial Teeth Scheduling Problem.
See ICAPS paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The MZN model was proposed by Felix Winter, with a Licence that seems to be like the MIT Licence.
Accompanying instances are based on real-life instances.

## Data Example
  05-0p15.json

## Model
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ATSP.py -data=<datafile.json>
  python ATSP.py -data=<datafile.dzn> -parser=ATSP_ParserZ.py
```

## Links
  - https://ojs.aaai.org/index.php/ICAPS/article/view/15997W
  - https://dbai.tuwien.ac.at/staff/winter/
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn21
