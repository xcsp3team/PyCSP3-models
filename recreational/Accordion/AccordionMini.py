"""
From Akgun et al.'s JAIR'25 paper:
    Accordion (BVS Development Corporation, 2017) is a single-player (patience or solitaire) card game.
    The game starts with the chosen cards in a sequence, each element of which we consider as a ‘pile’ of one card.
    Each move we make consists of moving a pile on top of either the pile immediately to the left, or three to the left
    (i.e. with two piles between the source and destination) such that the top cards in the source and destination piles match
    by either rank (value of the card, e.g. both 7) or suit (clubs, hearts, diamonds, or spades).
    The result of each move is to reduce the number of piles by 1 and change the top card of the destination pile.
    The empty space left at the position of the source pile is deleted.
    The goal is to keep making moves until just one pile remains.
    We consider the ‘open’ variant where the positions of all cards are known before play starts, in a variant studied by Ross and Knuth (1989)
    where we play with a randomly chosen subset of n ≤ 52 cards.
    A problem instance consists of the subset of cards in play, and their initial positions.

The model, below, is close to (can be seen as the close translation of) the one proposed in [Akgun et al. JAIR, 2025].
See Experimental Data for TabID Journal Paper (URL given below).

## Data Example
  11-01.json

## Model
  constraints: Element

## Execution
  python Accordion.py -data=<datafile.json>
  python Accordion.py -data=<datafile.txt> -parser=Accordion_ParserE.py

## Links
  - https://www.jair.org/index.php/jair/article/view/17032/27165
  - https://pure.york.ac.uk/portal/en/datasets/experimental-data-for-tabid-journal-paper

## Tags
  recreational, xcsp25
"""

from pycsp3 import *

cards = data or load_json_data("11-01.json")

n, nSteps = len(cards), len(cards)

# pf[t] is the pile which is moved from at time t
pf = VarArray(size=n - 1, dom=range(n))

# pt[t] is the pile which is moved to at time t
pt = VarArray(size=n - 1, dom=range(n))

# cf[t] is the top card of the pile which is moved from at time t
cf = VarArray(size=n - 1, dom=range(52))

# ct[t] is the top card of the pile which is moved to at time t
ct = VarArray(size=n - 1, dom=range(52))

# x[t][i] is the top card of the jth pile at time t
x = VarArray(size=[nSteps, n], dom=range(52))

T1 = build_table([range(n), range(n)], lambda v1, v2: (v1 == v2 - 1) or (v1 == v2 - 3))
T2 = build_table([range(52), range(52)], lambda v1, v2: (v1 % 13 == v2 % 13) or (v1 // 13 == v2 // 13))
T3 = lambda i: build_table([range(n), range(52), range(52)], lambda v1, v2, v3: not (i < v1) or (v2 == v3))
T4 = lambda i: build_table([range(n), range(n), range(52), range(52)], lambda v1, v2, v3, v4: not ((i > v1) and (i < v2)) or (v3 == v4))
T5 = lambda i: build_table([range(n), range(52), range(52)], lambda v1, v2, v3: not (i >= v1) or (v2 == v3))

satisfy(
    # setting initial state
    x[0] == cards,

    # making the move
    [
        (
            x[t][pf[t]] == x[t + 1][pt[t]],
            cf[t] == x[t][pf[t]],
            ct[t] == x[t][pt[t]]
        ) for t in range(n - 1)
    ],

    # ensuring each move is either 1 or three places
    [(pt[t], pf[t]) in T1 for t in range(n - 1)],

    # ensuring that the top cards of the two involved piles are of the same rank or suit
    [(cf[t], ct[t]) in T2 for t in range(n - 1)],

    # ensuring unmoved cards are copied from one timestep to the next one
    [
        [(pt[t], x[t][i], x[t + 1][i]) in T3(i) for t in range(n - 1) for i in range(n)],

        [(pt[t], pf[t], x[t][i], x[t + 1][i]) in T4(i) for t in range(n - 1) for i in range(n)],

        [(pf[t], x[t + 1][i], x[t][i + 1]) in T5(i) for t in range(n - 1) for i in range(n - 1)]
    ],

    # unused slots are filled up with zero
    x[1:, -1] == 0,

    [pf[t] <= n - t + 1 for t in range(n - 1)]
)
