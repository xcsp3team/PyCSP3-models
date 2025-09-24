# Problem: Portal

Portal game.

From the introduction of the model submitted to the 2024 mzn challenge.
The game is played on a 2D grid. The player can move up, down, left, or right.
The player can also shoot a portal in any direction. The portal will travel in a straight line until it hits a wall.
The player can then shoot a second portal. If they move onto a portal, they will be teleported to the other portal.
If they shoot a third portal, the first portal will disappear.
The player can only shoot one portal at a time. The player can only have two portals on the board at a time.
The player can only move one square at a time.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  rand-10-9-010.json

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Portal.py -data=<datafile.json>
```

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  recreational, mzn24

<br />

## _Alternative Model(s)_

#### Portal2.py
 - constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Table](https://pycsp.org/documentation/constraints/Table)
 - tags: recreational, mzn24
