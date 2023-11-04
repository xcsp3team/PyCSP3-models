# Problem CostasArray
## Description
This is the [problem 076](https://www.csplib.org/Problems/prob076/) of the CSPLib and a [NumberJack](https://github.com/eomahony/Numberjack) example.
A costas array is a pattern of n marks on an n∗n grid, one mark per row and one per column, in which the n∗(n−1)/2
vectors between the marks are all-different.

### Example

An example of a solution for n=7 is:
```
   4  3  6  2  0  7  1  5
```

## Data
a number n, the size of the grid.

## Model(s)

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Intension](http://pycsp.org/documentation/constraints/Intension)


## Command Line


```
python CostasArrays.py
python CostasArrays.py -data=10
```

## Tags
 academic csplib
