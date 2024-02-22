"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  02.json

## Model
  constraints: Regular

## Execution
  python Pentominoes2.py -data=<datafile.json>
  python Pentominoes2.py -data=<datafile.dzn> -parser=Pentominoes_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  recreational, mzn20
"""

from pycsp3 import *

width, height, tiles, dfa = data
nTiles = len(tiles)


def automaton_for(tile):
    q = Automaton.q
    nStates = tile[0]
    assert tile[1] == nTiles + 1
    trs = [(q(i + 1), j, q(dfa[tile[4] + i * (nTiles + 1) + j])) for i in range(nStates) for j in range(nTiles + 1) if dfa[tile[4] + i * (nTiles + 1) + j] != 0]
    return Automaton(start=q(1), final=[q(i) for i in range(tile[2], tile[3] + 1)], transitions=trs)


# x[k] is the tile number for the kth cell
x = VarArray(size=width * height, dom=range(nTiles + 1))

satisfy(
    # avoiding the special tile if not on the right border
    [x[h * width + w] != nTiles for h in range(height) for w in range(width - 1)],

    # putting the special tile on the right border
    [x[h * width + width - 1] == nTiles for h in range(height)],

    # ensuring each tile is present
    [x in automaton_for(tile) for tile in tiles]
)
