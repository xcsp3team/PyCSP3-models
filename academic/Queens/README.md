# Problem Queens
## Description
This is the [problem 054](https://www.csplib.org/Problems/prob054/) of the CSPLib:

"*Can n queens (of the same colour) be placed on a n×n chessboard so that none of the queens can attack each other?*"


### Example
A solution for n=8
![Queens](http://pycsp.org/assets/notebooks/figures/queens.png)

## Data
A number n, the size of the board.

## Model(s)


You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Queens/).

There are 3 variants of this problem, one with AllDifferent constraints, the other ones with constraint in intension.

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Intension](http://pycsp.org/documentation/constraints/Intension)

## Command Line
```
python Queens.py
python Queens.py -data=6
python Queens.py -data=6 -variant=v1
python Queens.py -data=6 -variant=v2
```

## Tags
 academic notebook csplib