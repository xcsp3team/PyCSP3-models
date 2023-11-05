# Problem Amaze3
## Description
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03-09.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count)

## Execution
  python Amaze3.py -data=<datafile.json>
  python Amaze3.py -data=<datafile.dzn> -parser=Amaze_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  recreational, mzn14, mzn19
