# Problem StableMarriage

Consider two groups of men and women who must marry.
Consider that each person has indicated a ranking for her/his possible spouses.
The problem is to find a matching between the two groups such that the marriages are stable.
A marriage between a man m and a woman w is stable iff:
 - whenever m prefers an other woman o to w, o prefers her husband to m
 - whenever w prefers an other man o to m, o prefers his wife to w

In 1962, David Gale and Lloyd Shapley proved that, for any equal number n of men and women,
it is always possible to make all marriages stable, with an algorithm running in O(n^2).

Nevertheless, this problem remains interesting
as it shows how a nice and compact model can be written.

## Data
  example.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution:
```
  python StableMarriage.py -data=<datafile.json>
```

## Tags
  recreational
