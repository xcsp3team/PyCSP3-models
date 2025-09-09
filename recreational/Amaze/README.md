# Problem: Amaze

Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line with horizontal or vertical segments,
while paying attention to not having crossed lines.

## Data Example
  simple.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Amaze.py -data=<datafile.json>
  python Amaze.py -data=<datafile.json> -keepHybrid
```

## Tags
  recreational, notebook

<br />

## _Alternative Model(s)_

#### Amaze_z1.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: recreational, mzn12
#### Amaze_z2.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element)
 - tags: recreational, mzn12
#### Amaze_z3.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count)
 - tags: recreational, mzn14, mzn19
