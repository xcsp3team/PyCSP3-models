# Problem GroupSplitter
## Description
A group of people want to do activities (Cinema then Restaurant) in subgroups
where the activities for subgroups are supposed to  match better members' preferences.
The aim of our model is to find the best activities and group combinations to recommend.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Jacopo Mauro and Tong Liu.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  u06g1p1.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  python GroupSplitter.py -data=<datafile.json>
  python GroupSplitter.py -data=<datafile.dzn> -parser=GroupSplitter_ParserZ.py

## Links
  - http://amsdottorato.unibo.it/9068/1/main.pdf
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn17, mzn19
