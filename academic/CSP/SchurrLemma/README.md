# Problem SchurrLemma
## Description
This is the [problem 015](https://www.csplib.org/Problems/prob015/) of the CSPLib.

"*The problem is to put n balls labelled 1...n into 3 boxes so that for any triple of balls (x,y,z) with x+y=z, not all are in the same box*".

The variant mod provided in the model is a variant proposed by  Bessiere Meseguer Freuder Larrosa,"On forward checking for non-binary constraint satisfaction", 2002.

### Example
A solution for 5 integers to put inside 4 boxes:
```
1 2 1 2 3
```

## Data
A couple \[n,d], n is the number of balls, d the number of boxes

## Model(s)
There are 3 variants of this problem, one with AllDifferent constraints, the other ones with constraint NValues.

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [NValues](http://pycsp.org/documentation/constraints/NValues)

## Command Line
```
  python SchurrLemma.py
  python SchurrLemma.py -data=[10,10]
  python SchurrLemma.py -data=[10,10] -variant=mod
```

## Tags
 academic csplib
