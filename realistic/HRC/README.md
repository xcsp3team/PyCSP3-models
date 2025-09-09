# Problem: HRC

The Hospitals/Residents problem with Couples (HRC) models the allocation of intending junior doctors to hospitals
where couples are allowed to submit joint preference lists over pairs of (typically geographically close) hospitals.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  exp1-1-5460.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python HRC.py -data=<datafile.json>
  python HRC.py -data=<datafile.dzn> -parser=HRC_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1007/s10601-016-9249-7
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn17, mzn19
