# Problem: Blocks

Blocks World Puzzle

Some numbered blocks are stacked into piles. The objective is to transform a start configuration into a goal configuration
by moving one block at a time, with a minimal number of moves.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Mats Carlsson, under the MIT Licence.

## Data Example
  16-4-05.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Element](https://pycsp.org/documentation/constraints/Element)

## Execution
```
  python Blocks.py -data=<datafile.json>
  python Blocks.py -data=<datafile.dzn> -parser=Blocks_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  recreational, mzn22
