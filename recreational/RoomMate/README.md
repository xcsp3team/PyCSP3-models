# Problem: RoomMate

In mathematics, economics and computer science, the stable-roommate problem is the problem of finding a stable matching for an even-sized set.
A matching is a separation of the set into disjoint pairs (‘roommates’).
The matching is stable if there are no two elements which are not roommates and which both prefer each other to their roommate under the matching.
This is distinct from the stable-marriage problem in that the stable-roommates problem allows matches between any two elements, not just between classes of
'men' and 'women'.

## Data Example
  sr0006.json

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python RoomMate.py -data=<datafile.json>
  python RoomMate.py -data=<datafile.json> -variant=table
  python RoomMate.py -data=<datafile.txt> -parser=RoomMate_Parser.py
```

## Links
  - https://en.wikipedia.org/wiki/Stable_roommates_problem
  - https://link.springer.com/chapter/10.1007/978-3-319-07046-9_2
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
