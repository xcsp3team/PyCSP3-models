# Problem InstructionSelection

Universal Instruction Selection.

Processors are built to execute a vast range of programs.
Techniques for instruction selection – the task of choosing the instructions for a given program – have not been so well studied.
This is the case in the PhD thesis of Gabriel Hjort Blindell in 2018,
with an approach that combines instruction selection with global code motion and block ordering.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2020 Minizinc challenges.
The MZN model was proposed by Gabriel Hjort Blindell (Copyright (c) 2013-2015)

## Data Example
  A3PZaPjnUz.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python InstructionSelection.py -data=<datafile.json>
  python InstructionSelection.py -data=<datafile.dzn> -parser=InstructionSelection_ParserZ.py
```

## Links
  - https://www.semanticscholar.org/paper/Universal-Instruction-Selection-Blindell/79f97178fb5493e0a1fe32073773de19faf22868
  - https://link.springer.com/chapter/10.1007/978-3-319-23219-5_42
  - https://link.springer.com/book/10.1007/978-3-319-34019-7
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn15, mzn20
