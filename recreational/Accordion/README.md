# Problem: Accordion

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
  constraints: [Element](https://pycsp.org/documentation/constraints/Element)

## Execution
```
  python Accordion.py -data=<datafile.json>
  python Accordion.py -data=<datafile.txt> -parser=Accordion_ParserE.py
```

## Links
  - https://www.jair.org/index.php/jair/article/view/17032/27165
  - https://pure.york.ac.uk/portal/en/datasets/experimental-data-for-tabid-journal-paper
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  recreational, xcsp25

<br />

## _Alternative Model(s)_

#### AccordionMini.py
 - constraints: [Element](https://pycsp.org/documentation/constraints/Element)
 - tags: recreational, xcsp25
