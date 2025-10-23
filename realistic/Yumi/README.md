# Problem: Yumi

Lightweight industrial robots such as YuMi by ABB Ltd. are designed to take over repetitive and tedious tasks from humans,
occupying similar floor area and having similar reach.
YuMi in particular caters to small-parts assembly manufacturing.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021/2022/2023/204 Minizinc challenges.
MIT Licence (Copyright 2021 Johan Ludde Wessénassumed)

## Data Example
  p-04-GG-GG-3.4.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [AllEqual](https://pycsp.org/documentation/constraints/AllEqual), [Count](https://pycsp.org/documentation/constraints/Count), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Yumi.py -data=<datafile.dzn> -parser=Yumi_ParserZ.py -variant=static
  python Yumi.py -data=<datafile.dzn> -parser=Yumi_ParserZ.py -variant=dynamic
```

## Links
  - https://new.abb.com/products/robotics/robots/collaborative-robots/yumi/dual-arm
  - https://link.springer.com/article/10.1007/s10601-023-09345-4
  - https://link.springer.com/chapter/10.1007/978-3-030-58942-4_33
  - https://github.com/LuddeWessen/assembly-robot-manager-minizinc
  - https://www.minizinc.org/challenge2021/results2021.html
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn21, mzn22, mzn23, mzn24
