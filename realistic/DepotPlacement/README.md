# Problem: DepotPlacement

Taken from the original Minizinc model:
"There are two warehouses, A and B. Each warehouse has a fixed set of customers.
No customer is served by both warehouses - so the two sets are disjoint.
Each warehouse has a truck. There is a table of distances from customer to warehouse and between the customers.

A truck is allowed to deliver not only to customers of its own warehouse, but also to customers of the other warehouse.
To make this possible there is a "depot" where one truck can leave some goods for the other truck to pick up and deliver to the customer.
The choice of depot is a decision variable ranging over customer and warehouse locations.

Naturally before delivering to a customer of another warehouse, the truck must first visit the depot to collect the goods for delivery to the customer.
The other truck must also visit the depot, of course, to drop off the goods.
There are no time constraints, and therefore no restriction on which truck visits the depot first.
The objective is to minimise the maximum of the distances travelled by the trucks."

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011/2016 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  rat-99-5.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Maximum](https://pycsp.org/documentation/constraints/Maximum)

## Execution
```
  python DepotPlacement.py -data=<datafile.json>
  python DepotPlacement.py -data=<datafile.dzn> -parser=DepotPlacement_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2016/results/

## Tags
  realistic, mzn10, mzn11, mzn16
