# Repository of PyCSP3 Models

PyCSP3 is a Python library allowing us to write models of combinatorial constrained problems in a declarative way.
See [pycsp3.org](https://pycsp3.org)

In this repository, you will find many models for various kinds of problems, from frameworks known as CSP (Constraint Satisfaction Problem) and COP (
Constraint Optimization Problem).
These models are classified in five main directories, listed below:

- academic: problems for which data are given by a fixed number of integers
- crafted: problems which have been designed for showing some specific feature(s)
- recreational: problems that have a playful nature while requiring some complex data structure
- realistic: problems that have a kind of industrial nature
- single: problems that are limited to a single instance

These problems/models mainly come from the literature/community, in particular from:

- scientific papers from top main conferences such as CP, CPAIOR, IJCAI, AAAI, ECAI, etc.
- [CSPLib](https://www.csplib.org/)
- [Minizinc Challenges](https://github.com/MiniZinc/mzn-challenge)
- [XCSP3 Compeitiions](https://xcsp.org/competitions/)

## Finding Models

In order to find specific models from our repository, you can use:

- [this page]() of PySCP3 website
- use the Python script 'searchmodels.py', at the root of theb main directory, whose usage is:

```
usage: python searchmodels.py [-constraint=Sum] [-tag=xcsp23] [-name='Bacp'] [-cop|csp] [-reverse] [-json|-file] [-showtags] [-showcontraints]

Extract problems with respect to a given query. You can mix different queries resulting to all problems that matches all queries. You can also reverse the results.

  -help display this help and exit
  -showtags show all available tags
  -showconstraints show all available constraints

  -constraint=Sum  extract all problems with Sum constraint
  -tag=xcsp2  extract all problems with tag containing xcsp2 (xcsp22, xcsp23...)
  -name=Ba extract all problems containing BA as a substring
  -cop|-csp extract  cop or csp problems
  -reverse reverse the results

  -json display results as a json file
  -github display results as links to github project
```

