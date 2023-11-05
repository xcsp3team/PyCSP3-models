"""
The model, below, is rebuilt from instances submitted to the 2013 Minizinc challenge.
These instances are initially given in flat format (i.e., not from a model).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  4-cube.json

## Model
  constraints: Clause

## Execution
  python Rubik.py -data=<datafile.json>
  python Rubik.py -data=<datafile.dzn> -parser=Rubik_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  crafted, mzn13
"""

from pycsp3 import *

n, clauses = data

# x[i] is the Boolean value of the ith variable
x = VarArray(size=n, dom={0, 1})

satisfy(
    # respecting all clauses
    Clause([x[abs(v) - 1] for v in clause], phases=[v > 0 for v in clause]) for clause in clauses
)

"""
1) ten solutions for 4-cube
2) one could also write:
  Clause(x[i] if b else ~x[i] for v in clause if (i := abs(v) - 1, b := v > 0)) for clause in clauses
"""
