# Problem SdnChain
## Description
Service Function Chain.

The problem is to deliver end-to-end networking services across multiple network domains
by implementing the so-called Service Function Chain (SFC) i.e., a sequence of Virtual Network Functions (VNF)
that composes the service.
See paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
It seems that the original MZN model was proposed by Liu, Tong, et al.
No Licence was explicitly mentioned (MIT Licence is assumed).

NB: We obtain the same bounds for all instances except for the instance d30 where we get 22 (with ACE and Choco) instead of 23.
After double checking, we didn't find what is the difference between the two models
TODO : problem with an instance (bound)

## Data Example
  d10n780-1.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SdnChain.py -data=<datafile.json>
  python SdnChain.py -data=<datafile.dzn> -parser=SdnChain_ParserZ.py
```

## Links
  - https://inria.hal.science/hal-02395208
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
