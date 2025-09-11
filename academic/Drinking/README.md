# Problem: Drinking

From Marriott & Stuckey "Programming with Constraints", exercise page 184, drinking game:
"In the drinking game, one must drink one glass everytime a number is reached which is divisible by 7 or divisible by 5,
unless the previous drink was taken less than 8 numbers ago."

The model, below, correspond to an optimization variant of this problem, used for the 2024 competition.

## Data
  a number n

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Drinking.py -data=number
```

## Links
  - https://www.hakank.org/common_cp_models/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, xcsp24
