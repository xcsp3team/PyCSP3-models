# Problem: MedianString

The median string problem is formulated as follows:
    Given a set of strings (of length at most equal to k) over a finite alphabet,
    find a string that minimizes the global edit distance to each of the given strings.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  p1-15-20-1.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MedianString.py -data=<datafile.json>
  python MedianString.py -data=<datafile.dzn> -parser=MedianString_ParserZ.py
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/0167865585900613
  - https://ojs.aaai.org/index.php/AAAI/article/view/5530
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn19
