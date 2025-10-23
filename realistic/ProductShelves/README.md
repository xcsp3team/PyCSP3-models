# Problem: ProductShelves

From Danyal Mirza (Ericsson): In a warehouse, a number of products are to be placed on some shelves such that the minimum amount of shelves is used.
These products are all shaped like 3-dimensional boxes, with dimensions length, width and height.
The shelves are also shaped like 3-dimensional boxes with dimensions length, width and height and the number of shelves are finite.
Neither the shelves and the products are allowed to be rotated.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original model was written by Danyal Mirza  from Ericsson (MIT Licence).

## Data Example
  toy.json

## Model
  constraints: [Lex](https://pycsp.org/documentation/constraints/Lex), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python ProductShelves.py -data=<datafile.json>
  python ProductShelves.py -data=<datafile.dzn> -parser=ProductShelves_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
