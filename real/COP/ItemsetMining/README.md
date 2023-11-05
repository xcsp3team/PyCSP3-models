# Problem ItemsetMining
## Description
A traditional task in machine learning is the task of concept learning.
Given a dataset of positive and negative examples, the aim is here to find a
formula in DNF (Disjunctive Normal Form) which characterizes the positive examples
as accurately as possible. Here, this task is modeled as a discrete constraint optimization problem;
the aim is to find a formula which is as accurate as possible.

The model is based on the link between DNF formulas and pattern sets in the data mining literature.
It represents the formula as a set of itemsets, and imposes constraints on both the itemsets and the set of itemsets.
It is based on the conference paper mentioned below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012/2013 Minizinc challenges.
The MZN model was proposed by the KULeuven team.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  anneal-k1.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum), [Lex](http://pycsp.org/documentation/constraints/Lex), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  python ItemsetMining.py -data=<datafile.json>
  python ItemsetMining.py -data=<datafile.dzn> -parser=ItemsetMining_ParserZ.py

## Links
  - http://dx.doi.org/10.1016/j.artint.2011.05.002
  - http://dtai.cs.kuleuven.be/CP4IM/
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  real, mzn11, mzn12, mzn13
