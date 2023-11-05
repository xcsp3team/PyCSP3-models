# Problem Zephyrus
## Description
The deployment optimization problem is the problem of how to correctly deploy all the software components
needed by a cloud application on suitable VMs on the cloud at minimal cost.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2019 challenges.
The MZN model was proposed by Jacopo Mauro (under the terms of the ISC License)
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  12-06-8-3.json

## Model
  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python Zephyrus.py -data=<datafile.json>
  python Zephyrus.py -data=<datafile.dzn> -parser=Zephyrus_ParserZ.py

## Links
  - https://bitbucket.org/jacopomauro/zephyrus2/src/master/
  - https://www.duo.uio.no/handle/10852/51754
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn16, mzn19
