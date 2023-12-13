# Problem ParityLearning
## Description
Optimization variant of the minimal disagreement parity (MDP) problem.

The MDP problem is introduced in the paper whose link is given below.
Given a set of sample input vectors and a set of sample parities, one has to
find the bits of the input vectors on which the parities were computed.
While the original problem is a satisfaction problem, in this variant,
one wants a solution that minimizes the number of errors.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  44-22-5-2.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ParityLearning.py -data=<datafile.json>
  python ParityLearning.py -data=<datafile.dzn> -parser=ParityLearning_ParserZ.py
```

## Links
  - https://www.cis.upenn.edu/~mkearns/papers/CrawfordKearnsSchapire.pdf
  - https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/DIMACS/PARITY/descr.html
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
