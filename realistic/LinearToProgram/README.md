# Problem LinearToProgram
## Description
This model finds a shortest program to compute a linear combination of variables.
The difficulty is that the program can only use the binary plus and the unary minus.
To symbolic program is linked to a set of examples against which it must conform.
This is one part of a counter-example guided loop, where examples are added when a counter example is found for the generated programs.
The counter-example generation is the other part and not included in this problem, which only does the program generation.
As an example, if the linear combination is -2 * p0 + -1 * p1 + 2 * p2, then a shortest program (among others) might be:
  - x3 = p0 + p0
  - x4 = p1 + x3
  - x5 = p2 + p2
  - x6 = - x4
  - x7 = x5 + x6
  - return x7

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013 Minizinc challenge.
The MZN model was proposed by Jean-Noel Monette, Uppsala University.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  l2p01.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python LinearToProgram.py -data=<datafile.json>
  python LinearToProgram.py -data=<datafile.dzn> -parser=LinearToProgram_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  realistic, mzn13
