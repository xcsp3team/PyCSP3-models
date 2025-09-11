# Problem: WordGolf

From Wikipedia:
    Word ladder (also known as Doublets, word-links, change-the-word puzzles, paragrams, laddergrams, or word golf) is a word game invented by Lewis Carroll.
    A word ladder puzzle begins with two words, and to solve the puzzle one must find a chain of other words to link the two, in which two adjacent words
    (that is, words in successive steps) differ by one letter.

## Data
  three integers and a dictionary filename

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python WorldGolf.py -data=[number,dict.txt,number,number]
  python WorldGolf.py -data=[number,dict.txt,number,number] -variant=mini
```

## Links
  - https://en.wikipedia.org/wiki/Word_ladder
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
