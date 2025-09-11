# Problem: SameQueensKnights

From archive.vector.org.uk
    In 1850, Carl Friedrich Gauss and Franz Nauck showed that it is possible to place eight queens on a chessboard such that no queen attacks any other queen.
    The problem of enumerating the 92 different ways there are to place 8 queens in this manner has become a standard programming example,
    and people have shown that it can be solved using many different search techniques.
    Now consider a variant of this problem: you must place an equal number of knights and queens on a chessboard such that no piece attacks any other piece.
    What is the maximum number of pieces you can so place on the board, and how many different ways can you do it?

A variant relaxes the fact that the number of queens and knights must be equal.
The variant "b" was used for the 2024 competition


## Data
  an integer n

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python SameQueensKnights.py -data=number
  python SameQueensKnights.py -data=number -variant=b
  python SameQueensKnights.py -data=number -variant=mini
```

## Links
  - http://archive.vector.org.uk/art10003900
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
