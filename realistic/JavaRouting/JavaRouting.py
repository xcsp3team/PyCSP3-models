"""
The model, below, is rebuilt from instances submitted to the 2013/2021 Minizinc challenges.
These instances are initially automatically generated from a problem description in Java.
For the original DZN files, no licence was explicitly mentioned (MIT Licence assumed).

The model, below, is an attempt to rebuild the original model from DZN files.
Unfortunately, we didn't find any information about the origin of this problem/model.

## Data Example
  trip6-3.json

## Model
  constraints: AllDifferent, Element

## Execution
  python JavaRouting.py -data=<datafile.json>
  python JavaRouting.py -data=<datafile.dzn> -parser=JavaRouting_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn13, mzn21
"""

from pycsp3 import *

choos, listg, chose, initi, mapge, cin, binop, objec, expec, celt, cad, cnot, expecX, cimp, listgX, mapgeX = data


def range_for(t, decrementing=False):
    return range(t[1][0], t[1][1] + 1) if not decrementing else range(t[1][0] - 1, t[1][1])


co = VarArray(size=len(choos), dom=lambda i: range_for(choos[i]))

ci = VarArray(size=len(chose), dom=lambda i: range_for(chose[i]))

il = VarArray(size=len(initi), dom=lambda i: range_for(initi[i]))

bo = VarArray(size=len(binop), dom=lambda i: range_for(binop[i]))

eat = VarArray(size=len(expec), dom=lambda i: range_for(expec[i]))

mg = VarArray(size=len(mapge), dom=lambda i: range_for(mapge[i]))

lg = VarArray(size=len(listg), dom=lambda i: range_for(listg[i]))

# for the three next arrays, values in domains are decreased (-1)

eatX = VarArray(size=len(expecX), dom=lambda i: range_for(expecX[i], True))

mgX = VarArray(size=len(mapgeX), dom=lambda i: range_for(mapgeX[i], True))

lgX = VarArray(size=len(listgX), dom=lambda i: range_for(listgX[i], True))

z = Var(dom=range_for(objec[0]))

# recording the specific name of each variable (in order to get access to them later by using the method 'var')
for t1, t2 in [(choos, co), (chose, ci), (mapge, mg), (expec, eat), (initi, il), (binop, bo), (listg, lg), (expecX, eatX), (mapgeX, mgX), (listgX, lgX)]:
    for i, (s, _, _) in enumerate(t1):
        t2[i].name(s)

satisfy(
    AllDifferent(var(name) for name in cad[0]),

    [var(name) in values for name, values in cin],

    [var(name1) >= var(name2) for name1, name2 in cnot],

    [
        If(
            var(name1) == v1,
            Then=var(name2) > v2
        ) for name1, v1, name2, v2 in cimp
    ],

    [var(name) == var(name1) + var(name2) for name, _, (name1, name2) in binop],

    [x[var(index)] == v for index, value, t in celt
     if (
         x := cp_array(e if isinstance(e, int) else var(e) for e in t),
         v := (value if isinstance(value, int) else var(value))
     )],

    z == var(objec[0][2][0]) + var(objec[0][2][1])
)

minimize(
    z
)
