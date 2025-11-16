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
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  recreational, xcsp25
"""

from pycsp3 import *

cards = data or load_json_data("11-01.json")

n, nSteps = len(cards), len(cards)
T, N = range(nSteps - 1), range(n)  # T used for iterating from 0 to nSteps-1 (excluded)

# pf[t] is the pile which is moved from at time t
pf = VarArray(size=nSteps - 1, dom=range(n))

# pt[t] is the pile which is moved to at time t
pt = VarArray(size=nSteps - 1, dom=range(n))

# cf[t] is the top card of the pile which is moved from at time t
cf = VarArray(size=nSteps - 1, dom=range(52))

# ct[t] is the top card of the pile which is moved to at time t
ct = VarArray(size=nSteps - 1, dom=range(52))

# x[t][i] is the top card of the jth pile at time t
x = VarArray(size=[nSteps, n], dom=range(52))

satisfy(
    # setting initial state
    x[0] == cards,

    # making the move
    [
        (
            x[t][pf[t]] == x[t + 1][pt[t]],
            cf[t] == x[t][pf[t]],
            ct[t] == x[t][pt[t]]
        ) for t in T
    ],

    # ensuring each move is either 1 or three places
    [
        either(
            pt[t] == pf[t] - 1,
            pt[t] == pf[t] - 3
        ) for t in T
    ],

    # ensuring that the top cards of the two involved piles are of the same rank or suit
    [
        either(
            cf[t] % 13 == ct[t] % 13,
            cf[t] // 13 == ct[t] // 13
        ) for t in T
    ],

    # ensuring unmoved cards are copied from one timestep to the next one
    [
        If(
            i < pt[t],
            Then=x[t][i] == x[t + 1][i]
        ) for t in T for i in N
    ] + [
        If(
            i > pt[t], i < pf[t],
            Then=x[t][i] == x[t + 1][i]
        ) for t in T for i in N
    ] + [
        If(
            i >= pf[t],
            Then=x[t + 1][i] == x[t][i + 1]
        ) for t in T for i in N[:-1]
    ],

    # unused slots are filled up with zero
    x[1:, -1] == 0,

    [pf[t] <= n - t + 1 for t in T]
)
