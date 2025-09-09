# Problem: PrizeCollecting

Variant of the prize collecting travelling salesman problem.
Here, a subtour is authorized (because there are negative costs).
See also the model in Minizinc

## Data Example
  25-5-5-9.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python PrizeCollecting.py -data=<datafile.json>
  python PrizeCollecting.py -data=<datafile.dzn> -variant=table
```

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic

<br />

## _Alternative Model(s)_

#### PrizeCollecting_z.py
 - constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn11, mzn16
