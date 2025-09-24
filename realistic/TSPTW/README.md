# Problem: TSPTW

Travelling Salesperson Problem with Time Windows (TSPTW).

From Lewander's paper cited below: Consider 𝑛 locations that are to be visited, where there is a travelling duration between each directed
pair of locations and there is for each location u an earliest visiting time etu and a latest visiting time ltu.
A travelling salesperson tour with time windows (TSPTW ) of size 𝑛 is a Hamiltonian path of the weighted directed graph induced by the 𝑛 locations as nodes,
visiting each location u exactly once and between times etu and ltu.
The departure time at the last-visited location is to be minimised.

This model is a simplified (but equivalent) version of TSPTW_z (submitted to the 2025 Minizinc challenge).

## Data Example
  n020w140-005.jso

## Model
  constraints: [Circuit](https://pycsp.org/documentation/constraints/Circuit), [Element](https://pycsp.org/documentation/constraints/Element)

## Execution
```
  python TSPTW.py -data=<datafile.json>
  python TSPTW.py -data=<datafile.dzn> -parser=TSPTW_ParserZ.py
```

## Links
  - https://www.jair.org/index.php/jair/article/view/17482
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic

<br />

## _Alternative Model(s)_

#### TSPTW_z.py
 - constraints: [Circuit](https://pycsp.org/documentation/constraints/Circuit), [Element](https://pycsp.org/documentation/constraints/Element)
 - tags: realistic, mzn25
