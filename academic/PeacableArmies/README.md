# Problem PeacableArmies

This is [Problem 110](https://www.csplib.org/Problems/prob110/) at CSPLib.

In the “Armies of queens” problem, we are required to place two equal-sized armies of black and white queens on a chessboard
so that the white queens do not attack the black queens (and necessarily vice versa) and to find the maximum size of two such armies.

## Example
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
  A number n, the size of the chessboard

## Model
  There are two variants "m1" and "m2"

  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python PeacableArmies.py -data=number -variant=m1
  - python PeacableArmies.py -data=number -variant=m2

## Tags
  academic, csplib
