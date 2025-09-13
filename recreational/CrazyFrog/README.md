# Problem: CrazyFrog

From LPCP contest 2021 (Problem 1):
    The problem is based on the Crazy Frog Puzzle.
    You have the control of a little frog, capable of very long jumps.
    The little frog just woke up in an SxS land, with few obstacles and a lot of insects.
    The frog can jump as long as you want, but only in the four cardinal directions (don't ask why) and you cannot land on any obstacle or already visited places.

Important: the model, below, has not been checked to exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data Example
  01.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Circuit](https://pycsp.org/documentation/constraints/Circuit), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python CrazyFrog.py -data=<datafile.json>
  python CrazyFrog.py -data=<datafile.json> -variant=table
```

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2021/tree/main/problem-1

## Tags
  recreational, lpcp21, xcsp25
