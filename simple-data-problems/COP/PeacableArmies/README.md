
# Problem Peacable Armies

## Description
This is the [problem 110](https://www.csplib.org/Problems/prob110/) of the CSPLib:

In the “Armies of queens” problem, we are required to place two equal-sized armies of black and white queens on a chessboard 
so that the white queens do not attack the black queens (and necessarily vice versa) and to find the maximum size of two such armies.

### Example
The optimum for a chessboard of size 8 is 9. 
A possible solution is

```
    W . . W W W . .
    . . . . W W . .
    W . . . . . . .
    W . . W . . . .
    . . . . . . B .
    . . . . . . B B
    . B B . . . . B
    . B B . . . B .
```


## Data
A number n, the size of the chessboard.

## Model(s)


There are two variants with two different models.

*Involved Constraints*: [Intension](https://pycsp.org/documentation/constraints/Intension/), [Count](https://pycsp.org/documentation/constraints/Count/), 
[Sum](https://pycsp.org/documentation/constraints/Sum/).


## Command Line
By default, PeacableArmies.py is in the directory problems/cop/academic/

```
python PeacableArmies.py -data=10 -variant=m1
python PeacableArmies.py -data=10 -variant=m2
```

## Some Results



| Data | Optimum |
|------|---------|
| 6    | 5       |
| 7    | 7       |
| 8    | 9       |
