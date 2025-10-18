"""
A traditional task in machine learning is the task of concept learning.
Given a dataset of positive and negative examples, the aim is here to find a
formula in DNF (Disjunctive Normal Form) which characterizes the positive examples
as accurately as possible. Here, this task is modeled as a discrete constraint optimization problem;
the aim is to find a formula which is as accurate as possible.

The model is based on the link between DNF formulas and pattern sets in the data mining literature.
It represents the formula as a set of itemsets, and imposes constraints on both the itemsets and the set of itemsets.
It is based on the conference paper mentioned below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012/2013 Minizinc challenges.
The original MZN model was proposed by the KULeuven team - no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  hepatitis-k2.json

## Model
  constraints: Count, Sum, Lex, Table

## Execution
  python ItemsetMining.py -data=<datafile.json>
  python ItemsetMining.py -data=<datafile.dzn> -parser=ItemsetMining_ParserZ.py

## Links
  - http://dx.doi.org/10.1016/j.artint.2011.05.002
  - http://dtai.cs.kuleuven.be/CP4IM/
  - https://www.minizinc.org/challenge/2013/results/

## Tags
  realistic, mzn11, mzn12, mzn13
"""

from pycsp3 import *

assert not variant() or variant("table")  # vatiant table only for k=1 for the moment

nItems, positiveExamples, negativeExamples, nSets = data or load_json_data("hepatitis-k2.json")  # nSets is the original k

nPos, nNeg = len(positiveExamples), len(negativeExamples)

assert nSets in (1, 2)

# precomputing three auxiliary complementary sets
posComplements = [[i for i in range(nItems) if i not in t] for t in positiveExamples]
negComplements = [[i for i in range(nItems) if i not in t] for t in negativeExamples]
itmComplements = [[j for j in range(nPos) if i not in positiveExamples[j]] for i in range(nItems)]

if nSets == 1:
    # x[i] is 1 if the ith item is selected
    x = VarArray(size=nItems, dom={0, 1})

    # tp[j] is 1 if the jth positive example is a true positive
    tp = VarArray(size=nPos, dom={0, 1})

    # tn[j] is 1 if the jth negative example is a true negative
    tn = VarArray(size=nNeg, dom={0, 1})

    if not variant():
        satisfy(
            # computing true positives
            [tp[j] == (Count(x[t]) == 0) for j, t in enumerate(posComplements) if len(t) > 0],

            # computing true negatives
            [tn[j] == (Count(x[t]) == 0) for j, t in enumerate(negComplements) if len(t) > 0],

            # computing selected items
            [x[i] == (Count(tp[t]) == 0) for i, t in enumerate(itmComplements) if len(t) > 0]
        )
    elif variant("table"):
        def table(r):
            return [(1, *[0] * r)] + [(0, *(1 if j == i else ANY for j in range(r))) for i in range(r)]


        satisfy(
            # computing true positives
            [(tp[j], x[t]) in table(r) for j, t in enumerate(posComplements) if (r := len(t)) > 0],

            # computing true negatives
            [(tn[j], x[t]) in table(r) for j, t in enumerate(negComplements) if (r := len(t)) > 0],

            # computing selected items
            [(x[i], tp[t]) in table(r) for i, t in enumerate(itmComplements) if (r := len(t)) > 0]
        )

    maximize(
        # maximizing correct discrimination
        Sum(tp) - Sum(tn)
    )

else:  # nSets = 2

    # x[k][i] is 1 if the ith item is selected in the kth set
    x = VarArray(size=[nSets, nItems], dom={0, 1})

    # tp[k][j] is 1 if the jth positive example is a true positive for the kth set
    tp = VarArray(size=[nSets, nPos], dom={0, 1})

    # tp[k][j] is 1 if the jth positive example is a true positive for the kth set
    tn = VarArray(size=[nSets, nNeg], dom={0, 1})

    jtp = VarArray(size=nPos, dom={0, 1})

    jtn = VarArray(size=nNeg, dom={0, 1})

    satisfy(
        # computing true positives
        [tp[k][j] == (Count(x[k][t]) == 0) for k in range(nSets) for j, t in enumerate(posComplements) if len(t) > 0],

        # computing true negatives
        [tn[k][j] == (Count(x[k][t]) == 0) for k in range(nSets) for j, t in enumerate(negComplements) if len(t) > 0],

        # computing selected items
        [x[k][i] == (Count(tp[k][t]) == 0) for k in range(nSets) for i, t in enumerate(itmComplements) if len(t) > 0],

        # computing joint true positives
        [jtp[t] == Exist(tp[:, t]) for t in range(nPos)],

        # computing joint true negatives
        [jtn[t] == Exist(tn[:, t]) for t in range(nNeg)],

        # tag(symmetry-breaking)
        [
            LexIncreasing(tp, strict=True),
            LexIncreasing(tn, strict=True)
        ]
    )

    maximize(
        # maximizing joint correct discrimination
        Sum(jtp) - Sum(jtn)
    )

""" Comments
0) BE CAREFUL: strict LexIncreasing discards some better solutions; this should be less or equal in a flawless model
1) using Count instead of Sum seems more efficient (because of the domain size of the auxiliary variables?)
2) using starred tables instead of Count is not efficient    
3) Count(x[t]) <= 0 is a shortcut for Count(x[i] for i in t) <= 0
   (tn[j], x[t]) is a shortcut for (tn[j], [x[i] for i in t])
4) Minizinc 2011, 2012 (k1 and k2 only differ from: K=1 or K=2) and 2013
"""
