# Problem: OncallRostering

A staff member must be assigned to each "day" in a rostering period.
A "day", means either one of Monday through to Thursday or all of Friday through Sunday; the latter is considered to be the weekend.
Individual staff members
  - may be unavailable on some days and may also be required to be on-call on some (other) days,
  - should ideally work the same number of week days and weekends over the rostering period,
  - should not be on-call for more than two days in a row (unless fixed in advance) and prefer not be on-call consecutive days in a row,
  - who are on-call over the weekend prefer not be on-call on the Wednesday before that weekend.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2018 Minizinc challenges.
The original MZN model was proposed by Julien Fischer -- no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  04s-010d.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python OncallRostering.py -data=<datafile.json>
  python OncallRostering.py -data=<datafile.dzn> -parser=OncallRostering_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2018/results/

## Tags
  realistic, mzn13, mzn18
