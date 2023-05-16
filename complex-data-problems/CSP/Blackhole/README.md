# Problem Blackhole

## Description
This is the [problem 081](http://www.csplib.org/Problems/prob081) of the CSPLib. This is the definition provided by wikipedia: 
"Black Hole is a solitaire card game. Invented by David Parlett, this game’s objective is to compress the entire 
deck into one foundation. The cards are dealt to a board in piles of three. The leftover card, dealt first or last, 
is placed as a single foundation called the Black Hole. This card usually is the Ace of Spades. Only the top cards of
each pile in the tableau are available for play and in order for a card to be placed in the Black Hole, it must be a 
rank higher or lower than the top card on the Black Hole. This is the only allowable move in the entire game. 
The game ends if there are no more top cards that can be moved to the Black Hole. The game is won if all of the
cards end up in the Black Hole.’’

Illustration of Black Hole (Solitaire). <small>Image from [commons.wikimedia.org](https://commons.wikimedia.org/wiki/File:Pysol-black-hole-solitaire-deal-1000-with-public-domain-tabletile.png)</small>
<img src="https://pycsp.org/assets/notebooks/figures/solitaire.png" alt="Solitaire" width="600" />

## Data
A tuple \[m,data.json], where m is the number of card per suit and the file data.json contains the position of cards.
This archive TODO contains different json files.

TODO a tuple ????  see command line ?
## Model(s)

You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Blackhole/).


*Involved Constraints*: [Channel](https://pycsp.org/documentation/constraints/Channel/), [Extension](https://pycsp.org/documentation/constraints/Extension/),
[Intension](https://pycsp.org/documentation/constraints/Intension/), [Increasing](https://pycsp.org/documentation/constraints/Increasing/).



## Command Line

```shell
python3 Blackhole.py -data=Blackhole-01.json
```

## Some Results

TODO

