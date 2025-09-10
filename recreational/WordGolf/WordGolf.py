"""
From Wikipedia:
    Word ladder (also known as Doublets, word-links, change-the-word puzzles, paragrams, laddergrams, or word golf) is a word game invented by Lewis Carroll.
    A word ladder puzzle begins with two words, and to solve the puzzle one must find a chain of other words to link the two, in which two adjacent words
    (that is, words in successive steps) differ by one letter.

## Data
  three integers and a dictionary filename

## Model
  constraints: Count, Table

## Execution
  python WorldGolf.py -data=[number,dict.txt,number,number]
  python WorldGolf.py -data=[number,dict.txt,number,number] -variant=mini

## Links
  - https://en.wikipedia.org/wiki/Word_ladder
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
"""

from pycsp3 import *
import random

m, dict_name, nSteps, seed = data

words = []
for line in open(dict_name):
    code = alphabet_positions(line.strip().lower())
    if len(code) == m:
        words.append(code)
words, nWords = cp_array(words), len(words)

random.seed(seed)
start, end = random.randint(0, nWords // 2), random.randint(nWords // 2, nWords)
print(words[start], words[end])

#  x[i][j] is the letter, number from 0 to 25, at row i and column j
x = VarArray(size=[nSteps, m], dom=range(26))

# y[i] is the word index of the ith word
y = VarArray(size=nSteps, dom=range(nWords))

# z is the number of steps
z = Var(range(nSteps))

satisfy(
    # setting the start word
    [
        x[0] == words[start],
        y[0] == start
    ],

    # setting the end word
    [
        x[-1] == words[end],
        y[-1] == end
    ],

    # setting the ith word
    [x[i] == words[y[i]] for i in range(1, nSteps - 1)]
)

if not variant():
    satisfy(
        # ensuring a (Hamming) distance of 1 between two successive words
        [
            If(
                i < z,
                Then=Hamming(x[i], x[i + 1]) == 1,
                Else=y[i] == y[i + 1]
            ) for i in range(nSteps - 1)
        ]
    )

elif variant("mini"):
    p = VarArray(size=nSteps - 1, dom=range(-1, m))

    Ts = [[(-1, ANY, ANY)] + [(j, v, w) for v in range(26) for w in range(26) if v != w] + [(k, v, v) for k in range(m) if k != j for v in range(26)] for j in
          range(m)]

    satisfy(
        [(z, p[i]) in [(v, -1) for v in range(i + 1)] + [(v, w) for v in range(i + 1, nSteps) for w in range(m)] for i in range(nSteps - 1)],

        [(p[i], x[i][j], x[i + 1][j]) in Ts[j] for j in range(m) for i in range(nSteps - 1)],

        [(z, y[i], y[i + 1]) in [(v, w, w) for v in range(i + 1) for w in range(nWords)] + [(v, ANY, ANY) for v in range(i + 1, nSteps)]
         for i in range(nSteps - 1)]
    )

satisfy(
    # setting the objective value (number of steps)
    y[z] == end
)

minimize(
    z
)

"""
1) Compilation Example: python WordGolf.py -data=[6,ogd2008,20,0]
"""

# python3 WordGolf.py -data=[6,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,0]
# python3 WordGolf.py -data=[7,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,0 => unsat non trivial
#   (seed 1, 2, 4 => unsat)
# python3 WordGolf.py -data=[7,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,3] => unsat non trivial
# 5 non trivial too
