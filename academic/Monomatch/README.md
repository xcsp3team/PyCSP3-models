# Problem Monomatch
## Description
Construction of a mono-matching game.

This type of game is most well-known as Dobble or Spot-It, and contains a set of cards with symbols on them.
Each pair of cards share a single symbol.

The model, below, is close to (can be seen as the close translation of) the one submitted to the M2021 inizinc challenge.
However, the original model involved set variables.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, with a MIT Licence.

## Data
  Two integers (n,p)

## Model
  There are two variants:
    - a main one with the constraint NValues,
    - a '01" variant with auxiliary variables

  Constraints: Count, Lex, NValues, Sum

## Execution
```
  python Monomatch.py -data=[number,number]
```

## Links
  - https://en.wikipedia.org/wiki/Dobble
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
