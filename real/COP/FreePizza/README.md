# Problem FreePizza
## Description
Taken from the Intelligent Systems course at Simon Fraser University.

The problem arises in the University College Cork student dorms. There is a large order
of pizzas for a party, and many of the students have vouchers for acquiring discounts in purchasing
pizzas. A voucher is a pair of numbers e.g. (2, 4), which means if you pay for 2 pizzas then you can
obtain for free up to 4 pizzas as long as they each cost no more than the cheapest of the 2 pizzas you
paid for. Similarly a voucher (3, 2) means that if you pay for 3 pizzas you can get up to 2 pizzas for
free as long as they each cost no more than the cheapest of the 3 pizzas you paid for. The aim is to
obtain all the ordered pizzas for the least possible cost. Note that not all vouchers need to be used.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  06.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python FreePizza.py -data=<datafile.json>
  python FreePizza.py -data=<datafile.dzn> -parser=FreePizza_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  real, mzn15
