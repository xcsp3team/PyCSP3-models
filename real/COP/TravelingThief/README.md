# Problem TravelingThief
## Description
Travelling Thief Problem

One has to visit all cities while picking items.
One has to maximize the value of the knapsack items and minimize the rental of the knapsack,
which depends on the travel time taking into account that the travel speed decreases with the weight of the items.
Note that there are no items in first city and there are always the same number of items in each other city.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n10-k03-c5000-l10000-u10100-r46.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python TravelingThief.py -data=sm-10-13-00.json
  python TravelingThief.py -data=sm-10-13-00.dzn -dataparser=TravelingThief_ParserZ.py

## Links
  - https://sites.google.com/view/ttp-gecco2023/home
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  real, mzn23
