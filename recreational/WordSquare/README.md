# Problem: WordSquare

From Wikipedia:
    A word square is a type of acrostic.
    It consists of a set of words written out in a square grid, such that the same words can be read both horizontally and vertically.
    The number of words, which is equal to the number of letters in each word, is known as the order of the square.

## Data
  an integer n, and a dictionary

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [AllDifferentList](https://pycsp.org/documentation/constraints/AllDifferentList), [Element](https://pycsp.org/documentation/constraints/Element), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python WordSquare.py -data=<datafile.json>
  python WordSquare.py -data=[number,dict.txt]
  python WordSquare.py -data=[number,dict.txt] -variant=hak
  python WordSquare.py -data=[number,dict.txt] -variant=tab1
  python WordSquare.py -data=[number,dict.txt] -variant=tab2
```

## Links
  - https://en.wikipedia.org/wiki/Word_square
  - https://github.com/matevz-kovacic/word-square?tab=readme-ov-file
  - https://www.hakank.org/minizinc/word_square.mzn
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  recreational, xcsp24
