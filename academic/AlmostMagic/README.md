# Problem: AlmostMagic

From JaneStreet:
    An almost magic square is, well, almost a magic square.
    It differs from a magic square in that the 8 sums may differ from each other by at most 1.
    For this puzzle, place distinct positive integers into the empty grid above such that each of four bold-outlined 3-by-3 regions is an almost magic square.
    Your goal is to do so in a way that minimizes the overall sum of the integers you use.


## Data
  two numbers n and p

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python AlmostMagic.py -data=[number,number]
  python AlmostMagic.py -data=[number,number] -variant=opt
```

## Links
  - https://www.janestreet.com/puzzles/almost-magic-index/

## Tags
  academic, janestreet, xcsp25
