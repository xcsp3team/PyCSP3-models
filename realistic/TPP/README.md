# Problem: TPP

The goal of the asymmetric travelling purchaser problem is to decide where to buy each of a set of products,
and in which order to visit the purchase locations, in order to minimize the total travel and purchase costs.
Travel costs are asymmetric, and cities are laid out on a grid with travel only allowed between horizontally and vertically adjacent cities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012/2016 Minizinc challenges.
The MZN model was proposed by Kathryn Francis.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-3-30-1.json

## Model
  constraints: [Circuit](https://pycsp.org/documentation/constraints/Circuit), [Element](https://pycsp.org/documentation/constraints/Element)

## Execution
```
  python TPP.py -data=<datafile.json>
  python TPP.py -data=<datafile.dzn> -parser=TPP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn12, mzn16
