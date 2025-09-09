# Problem: CryptoPuzzle

Verbal arithmetic, also known as alphametics, cryptarithmetic, cryptarithm or word addition, is a type of mathematical game
consisting of a mathematical equation among unknown numbers, whose digits are represented by letters of the alphabet.

### Example
  For the Puzzle:
  ```
       S E N D
   +   M O R E
   = M O N E Y
  ```
  a possible solution is:
  ```
       9 5 6 7
   +   1 0 8 5
   = 1 0 6 5 2
  ```

## Data
  Three strings/words (as for example [send,more,money])

## Model
  There are a main variant and a variant involving carry variables.
  You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/CryptoPuzzle/).

  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CryptoPuzzle.py -data=[string,string,string]
  python CryptoPuzzle.py -data=[string,string,string] -variant=carry
```

## Links
  - https://en.wikipedia.org/wiki/Verbal_arithmetic

## Tags
  academic, notebook
