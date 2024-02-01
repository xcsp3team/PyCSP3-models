# Problem Langford

This is [Problem 024](https://www.csplib.org/Problems/prob024/) at CSPLib.

Consider two sets of the numbers from 1 to 4.
The problem is to arrange the eight numbers in the two sets into a single sequence in which:
  - the two 1’s appear one number apart,
  - the two 2’s appear two numbers apart,
  - the two 3’s appear three numbers apart,
  - and the two 4’s appear four numbers apart.

### Example
  A graphical representation of L(2,4) with black=1, red=2, blue=3 and yellow=4 (source CSPLib)
  ![langford](https://www.csplib.org/Problems/prob024/assets/langford.gif)

## Data
  A pair (k,n), where n is the number of values and k the number of occurrences for a value

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent)

## Execution
```
  python Langford.py -data=[number,number]
```

## Links
  - https://www.csplib.org/Problems/prob024

## Tags
  academic, csplib
