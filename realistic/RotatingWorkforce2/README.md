# Problem RotatingWorkforce2

Rotating workforce scheduling problem.
See paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Mikael Zayenz Lagerkvist, under the MIT Licence.

## Data Example
  e025s7.json

## Model
  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Regular](http://pycsp.org/documentation/constraints/Regular), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python RotatingWorkforce2.py -data=<datafile.json>
  python RotatingWorkforce2.py -data=<datafile.dzn> -dataparser=RotatingWorkforce2_ParserZ.py
```

## Links
  - https://www.semanticscholar.org/paper/2-The-Rotating-Workforce-Scheduling-Problem-Musliu-Schutt/4048daa6fe7917009174dab7f3fe84e84fdc36dd
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
