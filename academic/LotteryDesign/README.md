# Problem: LotteryDesign

X is a set of balls labelled 1 to d.
Find a set B of n tickets each containing m of these numbers, such that for any draw D of p distinct
balls from X, we can find at least one ticket B ∈ B which matches D in at least t places.

Important: the model, below, does not exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data
   five numbers: d, m, p, t, n

## Model
  constraints: [AllDifferentList](https://pycsp.org/documentation/constraints/AllDifferentList)

## Execution
```
  python LotteryDesign.py -data=[number,number,number,number,number]
```

## Links
  - https://doi.org/10.1007/s10601-024-09368-5

## Tags
  realistic, xcsp25

<br />

## _Alternative Model(s)_

#### LotteryDesignMini.py
 - constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent)
 - tags: realistic, xcsp25
