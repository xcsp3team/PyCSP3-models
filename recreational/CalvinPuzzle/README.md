# Problem CalvinPuzzle

The purpose of the game is to fill a grid of size n × n with all values ranging from 1 to n*n such that:
  - if the next number in the sequence is going to be placed vertically or horizontally, then it must be placed exactly three squares away
  from the previous number (there must be a two square gap between the numbers);
  - if the next number in the sequence is going to be placed diagonally, then it must be placed exactly two squares away
  from the previous number (there must be a one square gap between the numbers).

## Data
  A unique integer n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Count](http://pycsp.org/documentation/constraints/Count), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python CalvinPuzzle.py -data=number
  - python CalvinPuzzle.py -data=number -variant=table

## Links
  - https://chycho.blogspot.com/2014/01/an-exercise-for-mind-10-by-10-math.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
