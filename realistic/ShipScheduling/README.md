# Problem ShipScheduling
## Description
From the ICAPS conference paper (whose reference is given below):
"Ship scheduling deals with assigning arrival and departure times to a ﬂeet of ships,
as well as the amount and sometimes type of cargo that is carried on each ship.
One consideration in ship scheduling which does not occur in other transportation problems is that most ports have
restrictions on the draft of ships that may safely enter the port.
Draft is the distance between the waterline and the ship’s keel, and is a function of the amount of cargo loaded onto the ship."

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012/2014 Minizinc challenges.
The MZN model was proposed by Elena Kelareva.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-Ships.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python ShipScheduling.py -data=<datafile.json>
  python ShipScheduling.py -data=<datafile.dzn> -parser=ShipScheduling_ParserZ.py
```

## Links
  - https://ojs.aaai.org/index.php/ICAPS/article/view/13494
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn11, mzn12, mzn14
