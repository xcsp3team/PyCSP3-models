# Problem: FoolSolitaire

An optimisation variation of Peg Solitaire (named Fool’s Solitaire by Berlekamp, Conway and Guy)
is to reach a position where no further moves are possible in the shortest sequence of moves.

The model is written for the English style board (standard), with 33 holes

## Data
  Two integers

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python FoolSolitaire.py -data=[number,number]
  python FoolSolitaire.py -data=[number,number] -variant=dec1
  python FoolSolitaire.py -data=[number,number] -variant=dec2
  python FoolSolitaire.py -data=[number,number] -variant=table
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054805000195
  - https://www.routledge.com/Winning-Ways-for-Your-Mathematical-Plays-Volume-2/Berlekamp-Conway-Guy/p/book/9781568811420
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
