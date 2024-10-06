"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  execute 'python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py -export' to get JSON files

## Model
  constraints: AllDifferent, Element, Sum

## Execution
  python CrosswordsOpt.py -data=<datafile.json>
  python CrosswordsOpt.py -data=<datafile.dzn> -parser=CrosswordsOpt_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  recreational, mzn17
"""

from pycsp3 import *

grid, clues, dictionary = data
n, m, nClues = len(grid), len(grid[0]), len(clues)

# values associated with letters
values = cp_array(1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10)


def well_formed_word_for(k, clue):
    scp = x[clue.row:clue.row + clue.length, clue.col] if clue.down == 1 else x[clue.row, clue.col:clue.col + clue.length]
    r = len(scp)
    assert r == clue.length
    words = dictionary[r]
    return [scp[i] == words[:, i][w[k]] for i in range(r)]
    # return [scp[i] == words[w[k], i] for i in range(len(scp))] takes much longer time


# x[i][k] is the letter (position in the alphabet) in the cell with coordinates (i,j)
x = VarArray(size=[n, m], dom=range(26))

# w[k] is the index of the word used for the kth clue
w = VarArray(size=nClues, dom=lambda k: range(len(dictionary[clues[k].length])))

satisfy(
    #  a word can appear only once
    [AllDifferent(w[k] for k, clue in enumerate(clues) if clue.length == v) for v in range(2, 23)],

    # black cells are arbitrarily assigned the letter 'a' (0)
    [x[i][j] == 0 for i in range(n) for j in range(m) if grid[i][j] == 0],

    # ensuring a well-formed word for each clue
    [well_formed_word_for(k, clue) for k, clue in enumerate(clues)]
)

maximize(
    # maximizing the values of letters put in the grid
    Sum(values[x[i][j]] for i in range(n) for j in range(m))
)

""" Comments
1) TODO: if  range(max_words + 1) it seems that posted element constraints are not valid (tuple with * although it seems that they should not be present)
2) It seems that it would be more efficient to use table constraints (to be tried) 
"""
