# Problem: MaximumDensityOscillatingLife

From CP'10 paper whose URL is given below:
    Conway’s Game of Life was invented by John Horton Conway.
    The game is played on a square grid. Each cell in the grid is in one of two states (alive or dead).
    The state of the board evolves over time: for each cell, its new state is determined by its
    previous state and the previous state of its eight neighbours (including diagonal neighbours).
    Oscillators are patterns that return to their original state after a number of steps (referred to as the period).
    A period 1 oscillator is named a still life. Here we consider the problem of finding oscillators of various periods.

## Data
  two numbers n and h

## Model
  constraints: [AllDifferentList](https://pycsp.org/documentation/constraints/AllDifferentList), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python MaximumDensityOscillatingLife.py -data=[number,number]
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-642-15396-9_19
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, xcsp24
