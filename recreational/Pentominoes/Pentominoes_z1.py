"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008/2011/2013 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  02.json

## Model
  constraints: Regular

## Execution
  python Pentominoes_z1.py -data=<datafile.json>
  python Pentominoes_z1.py -data=<datafile.dzn> -parser=Pentominoes_ParserZ.py

## Links
  - https://fr.wikipedia.org/wiki/Pentomino
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  recreational, mzn08, mzn11, mzn13
"""

from pycsp3 import *
from pycsp3.problems.data.parsing import split_with_rows_of_size

m, n, tiles, dfa = data or load_json_data("02.json")

nTiles = len(tiles)
SEP = nTiles + 1


def A(tile):  # automaton for given tile
    n_states, n_symbols = tile[0], tile[1]
    t = split_with_rows_of_size(dfa[tile[-1]:tile[-1] + n_states * n_symbols], n_symbols)
    q = Automaton.q  # for building names of states
    trs = [(q(i), j, q(t[i - 1][j - 1])) for i in range(1, n_states + 1) for j in range(1, n_symbols + 1) if t[i - 1][j - 1] != 0]
    return Automaton(start=q(1), final=[q(i) for i in range(tile[2], tile[3] + 1)], transitions=trs)


# x[i][j] is the index of the tile in the cell with coordinates (i,j)
x = VarArray(size=[n, m], dom=range(1, nTiles + 2))

satisfy(
    # forbidding the special symbol if not at the end of a row
    [x[i][j] != SEP for i in range(n) for j in range(m - 1)],

    # setting the special symbol at the end of each row
    [x[i][-1] == SEP for i in range(n)],

    # ensuring each tile is present
    [x in A(tile) for tile in tiles]
)

""" Comments
1) Note that x is automatically flattened when posting the Regular constraints

2) In Minizinc challenges 2008, 2011 and 2013: same instances in 2011 and 2013; two original additional instances in 2008
"""
