# Problem PrizeCollecting

Variant of the prize collecting travelling salesman problem.
Here, a subtour is authorized (because there are negative costs).
See also the model in Minizinc

## Data Example
  25-5-5-9.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

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

## _Alternative Models_

#### PrizeCollecting_z.py
 - constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn11, mzn16
