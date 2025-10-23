# Problem: ATSP

Artificial Teeth Scheduling Problem.
See ICAPS paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Felix Winter, with a Licence that seems to be like the MIT Licence.
Accompanying instances are based on real-life instances.

## Data Illustration
  05-0p15.json

## Model
  constraints: [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ATSP.py -data=<datafile.json>
  python ATSP.py -data=<datafile.dzn> -parser=ATSP_ParserZ.py
```

## Links
  - https://ojs.aaai.org/index.php/ICAPS/article/view/15997W
  - https://dbai.tuwien.ac.at/staff/winter/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn21, mzn25
