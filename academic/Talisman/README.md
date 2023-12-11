# Problem Talisman
## Description
An n x n array  of the integers from 1 to n^2 such that the difference between any integer
and its neighbor (horizontally, vertically, or diagonally, without wrapping around)
is greater than or equal to some value k is called a (n,k)-talisman square.

## Example
  A solution for the (4,2)-talisman square:
  ```
      1  8 11 14
      4 16  5  2
     12  9 13 10
     15  6  3  7
  ```

## Data
  A pair (n,k).

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent)

## Execution
```
  python Talisman.py -data=[number,number]
```

## Links
  - https://mathworld.wolfram.com/TalismanSquare.html

## Tags
  academic
