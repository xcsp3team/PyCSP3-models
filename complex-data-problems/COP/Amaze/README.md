# Problem Amaze

## Description

See Problem in [MiniZinc](https://github.com/MiniZinc/minizinc-benchmarks/tree/master/amaze)

Given a grid containing pairs of numbers (ranging from 1 to a greater value), connect the pairs (e.g. 1 to 1; 2 to 2; etc)
by drawing a line horizontally and vertically, but not diagonally.
The lines must never cross.


## Data
The file Amaze_simple.json contains an example of data.


## Model

*Involved Constraints*: [Count](https://pycsp.org/documentation/constraints/Count) [Sum](https://pycsp.org/documentation/constraints/Sum) [Extension](https://pycsp.org/documentation/constraints/Extension) [Intension](https://pycsp.org/documentation/constraints/Intension)


## Command Line

```shell
python3 Amaze.py -data=Amaze_simple.json [-solve]
```


