# Problem KnightTour
## Description
You can see below, the beginning of the description provided by  [wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour).

"*A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly
once. If the knight ends on a square that is one knight's move from the beginning square (so that it could tour the board again immediately, following the same path), the tour is closed; otherwise, it is open.*".

### Example
This is an animation of on _open_ knigth tour on a 5x5 board (source: [wikipedia](https://en.wikipedia.org/wiki/Knight%27s_tour))

![knight tour](https://upload.wikimedia.org/wikipedia/commons/c/ca/Knights-Tour-Animation.gif)

## Data
A number n, the size of the board.

## Model(s)
There are three variant, one with only constraint in intension, two with constraint in extension.

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Extension](http://pycsp.org/documentation/constraints/Extension), [Intension](http://pycsp.org/documentation/constraints/Intension)

## Command Line
```
  python KnightTour.py
  pythongithub KnightTour.py -data=16
  python KnightTour.py -data=16 -variant=table-2
  python KnightTour.py -data=16 -variant=table-3
```

## Tags
 academic
