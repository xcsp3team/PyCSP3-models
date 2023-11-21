"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Mikael Zayenz Lagerkvist, with a MIT Licence.

## Data Example
  s05-t20-s17-close.json

## Model
  The automatas may be non-deterministic. This is why we have two variants:
    - a main one
    - a variant called "det"

  constraints: Regular

## Execution
  python PentominoesZayenz.py -data=sm-10-13-00.json
  python PentominoesZayenz.py -data=sm-10-13-00.dzn -dataparser=PentominoesZayenz_ParserZ.py

## Links
  - https://www.researchgate.net/publication/228523019_Modeling_irregular_shape_placement_problems_with_regular_constraints
  - https://github.com/zayenz/minizinc-pentominoes-generator
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn21
"""

from pycsp3 import *

size, tiles = data
nTiles = len(tiles)


def automaton(i):
    def part(pivot, path, offset, transitions):
        others = ne(pivot)  # [v for v in range(nTiles + 1) if v != pivot]
        last = q(0)
        for tok in path.split(" "):
            if tok[0] == 'A':
                if len(tok) == 2:
                    assert tok[-1] == "*"
                    transitions.append((last, others, last))
                else:
                    nb = 1 if len(tok) == 1 else int(tok[2:-1])
                    for _ in range(nb):
                        offset += 1
                        transitions.append((last, others, q(offset)))
                        last = q(offset)
            else:
                t = tok.split("{")
                assert int(t[0]) == pivot, str(pivot) + t[0]
                nb = 1 if len(t) == 1 else int(t[1][:-1])
                for _ in range(nb):
                    offset += 1
                    transitions.append((last, pivot, q(offset)))
                    last = q(offset)
        return offset

    q = Automaton.q  # for building state names
    transitions, final = [], []
    offset = 0
    for p in list(dict.fromkeys([v.strip()[1:-1] for v in tiles[i].split("|")])):  # we remove duplicates
        offset = part(i + 1, p, offset, transitions)
        final.append(q(offset))
    return Automaton(start=q(0), final=final, transitions=transitions)


# x[i][j] is the index of the tile in the cell with coordinates (i,j)
x = VarArray(size=[size, size + 1], dom=range(nTiles + 1))

satisfy(
    # forbidding the special symbol 0 if not at the end of a row
    [x[i][j] != 0 for i in range(size) for j in range(size)],

    # setting the special symbol 0 at the end of each row
    [x[i][size] == 0 for i in range(size)],

    # ensuring each tile is present
    [x in (A.deterministic_copy(x) if variant("det") else A) for i in range(nTiles) if (A := automaton(i))]
)

"""
1) The automatas may be non-deterministic. This is why we have two variants.
2) generating the deterministic automatas may be very long
"""
