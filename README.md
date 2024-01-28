# PyCSP3 Models (and Data)


**WARNING.** *Currently, the site pycsp.org is not available. This is due to a payment problem, and as we follow **soviet-like procedures** here in France (most of the time, we must use purchase orders), this may take some time. 
For the same kind of reasons, I have decided to limit/cancel my missions, as with CNRS, each mission requires a couple of hours for just filling forms. **This is not acceptable** (especially for the administrative agents who endure this Kafkaian world; some of them becoming depressed). I agree that our working environment is **not professional**.*

PyCSP3 is a Python library allowing us to write models of combinatorial constrained problems in a declarative way.
See [pycsp3.org](https://www.pycsp.org/)

In this repository, you will find **more than 300 models** for various kinds of problems, together with some data files, from frameworks known as CSP (Constraint Satisfaction Problem) and COP (
Constraint Optimization Problem).
These models are classified in five main directories:

- academic: problems for which data are given by a fixed number of elementary values (typically, integers)
- crafted: problems which have been designed for showing some specific feature(s)
- recreational: problems that have a playful nature while requiring some complex data structure (i.e., not elementary values)
- realistic: problems that have a kind of industrial nature
- single: problems that are limited to a single instance

These problems/models mainly come from the literature/community, in particular from:

- scientific conference papers, typically from top main conferences such as CP, CPAIOR, IJCAI, AAAI, ECAI, ... 
- scientific jounral papers, typically from top main journals such as Constraints, AIJ, JAIR, ...
- [XCSP3 Competitions](https://xcsp.org/competitions/)
- [CSPLib](https://www.csplib.org/)
- [Minizinc Challenges](https://github.com/MiniZinc/mzn-challenge)
- [LPCP Contests](https://github.com/lpcp-contest)

## Finding Models

In order to find specific models from our repository, you can use:

- [this page]() from PySCP3 website
- use the Python script 'searchmodels.py', at the root of theb main directory, whose usage is:

```
usage: python searchmodels.py [-constraint=Sum] [-tag=xcsp23] [-name='Bacp'] [-cop|csp]
                              [-reverse] [-json|-file] [-showtags] [-showcontraints]

Extract problems with respect to a given query.
You can mix different queries resulting to all problems that matches all queries.
You can also reverse the results.

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

