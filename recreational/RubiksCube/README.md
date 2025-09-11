# Problem: RubiksCube

The 1D Rubik’s Cube is a vector composed of 6 number, which can be rotated in 3 different ways in groups of four.
The problem associated with the 1D Rubik’s Cube can be defined in general terms:
given a scrambled vector V of size n, the objective is to return the shortest sequence of rotations (of length g) so as to restore the original ordered vector.

## Data
  An integer (or four integers)

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent)

## Execution
```
  python RubiksCube.py -data=<datafile.json>
  python RubiksCube.py -data=[number,number,number,number]
```

## Links
  - https://www.mail-archive.com/programming@jsoftware.com/msg05817.html
  - http://www.hakank.org/picat/1d_rubiks_cube.pi
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
