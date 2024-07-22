"""
A logic puzzle. See "Shikaku as a Constraint Problem" by Helmut Simonis.

## Data Example
  grid01.json

## Model
  constraints: Table

## Execution:
  python Shikaku.py -data=<datafile.json>

## Links
 - https://en.wikipedia.org/wiki/Shikaku

## Tags
  recreational
"""

from pycsp3 import *

nRows, nCols, rooms = data
nRooms = len(rooms)


def no_overlapping(i, j):
    leftmost = i if rooms[i].col <= rooms[j].col else j
    rightmost = j if leftmost == i else i
    p = rgt[leftmost] <= lft[rightmost]
    if rooms[leftmost].row == rooms[rightmost].row:
        return p
    if rooms[leftmost].row > rooms[rightmost].row:
        return p | (top[leftmost] >= bot[rightmost])
    return p | (bot[leftmost] <= top[rightmost])


# lft[i] is the position of the left border of the ith room
lft = VarArray(size=nRooms, dom=range(nCols + 1))

# rgt[i] is the position of the right border of the ith room
rgt = VarArray(size=nRooms, dom=range(nCols + 1))

# top[i] is the position of the top border of the ith room
top = VarArray(size=nRooms, dom=range(nRows + 1))

# bot[i] is the position of the bottom border of the ith room
bot = VarArray(size=nRooms, dom=range(nRows + 1))

satisfy(
    # each room must be surrounded by its borders
    [
        (
            lft[i] <= col,
            rgt[i] > col,
            top[i] <= row,
            bot[i] > row
        ) for i, (row, col, _) in enumerate(rooms)
    ],

    # respecting the surface of each room
    [(rgt[i] - lft[i]) * (bot[i] - top[i]) == v for i, (_, _, v) in enumerate(rooms)],

    # rooms must not overlap
    [no_overlapping(i, j) for i, j in combinations(nRooms, 2)]
)

""" Comments
1) It is also possible to write (but this is less compact):
 [lft[i] <= rooms[i].col for i in range(nRooms)],
 [rgt[i] > rooms[i].col for i in range(nRooms)],
 [top[i] <= rooms[i].row for i in range(nRooms)],
 [bot[i] > rooms[i].row for i in range(nRooms)],
"""
