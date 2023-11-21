# Problem NonTransitiveDice
## Description
A set of dice is intransitive if the binary relation “X rolls a higher number than Y more than half the time” on its elements is not transitive.
This situation is similar to that in the game Rock, Paper, Scissors, in which each element has an advantage over one choice and a disadvantage to the other.
The problem is to exhibit such a set of dice.

## Data
  three integers: n, m and d

## Model
  constraints: [Maximum](http://pycsp.org/documentation/constraints/Maximum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python NonTransitiveDice.py -data=[number,number,number]
  - python NonTransitiveDice.py -data=[number,number,number] -variant=opt

## Links
  - https://en.wikipedia.org/wiki/Intransitive_dice
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
