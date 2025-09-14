# Problem: ChainReaction

From JaneStreet:
    Write down a chain of integers between 1 and 100, with no repetition, such that if x and y are consecutive numbers in the chain,
    then x evenly divides y or y evenly divides x. Here is an example of such a chain, with length 12:
      37, 74, 2, 8, 4, 16, 48, 6, 3, 9, 27, 81
    What is the longest chain you can find?

## Data
  two numbers n and k

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ChainReaction.py -data=[number,number]
  python ChainReaction.py -data=[number,number] -variant=opt
```

## Links
  - https://www.janestreet.com/puzzles/chain-reaction-index/

## Tags
  academic, janestreet, xcsp25
