# Problem WaterBucket
## Description
This is the [problem 018](https://www.csplib.org/Problems/prob018/) of the CSPLib:

You are given an 8 pint bucket of water, and two empty buckets which can contain 5 and 3 pints respectively. You are required to divide the water into two by pouring water between buckets (that is, to end up with 4 pints in the 8 pint bucket, and 4 pints in the 5 pint bucket).

What is the minimum number of transfers of water between buckets?


## Data
a tuple \[c1, c2, c3, g1, g2, g3, h], where
- c1, c2, c3 for capacities of the three buckets
- g1, g2, g3  for goal (which quantities must be present in the three buckets after all transfers)
- h for horizon (maximal number of rounds/transfers)

## Model(s)


  constraints: [Extension](http://pycsp.org/documentation/constraints/Extension)


## Command Line

```
python WaterBucket.py
python WaterBucket.py -data=[8,5,3,4,4,0,8]
```

## Tags
 academic

