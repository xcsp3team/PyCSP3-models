# Problem ProgressiveParty

See Problem 013 on CSPLib.

The problem is to timetable a party at a yacht club.
Certain boats are to be designated hosts, and the crews of the remaining boats in turn visit the
host boats for several successive half-hour periods. The crew of a host boat remains on board
to act as hosts while the crew of a guest boat together visits several hosts. Every boat can only
hold a limited number of people at a time (its capacity) and crew sizes are different. The total
number of people aboard a boat, including the host crew and guest crews, must not exceed the
capacity. A table with boat capacities and crew sizes can be found below; there were six time
periods. A guest boat cannot not revisit a host and guest crews cannot meet more than once.
The problem facing the rally organizer is that of minimizing the number of host boats.

## Data Example
  12-05.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Channel](http://pycsp.org/documentation/constraints/Channel), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python ProgressiveParty.py -data=<datafile.json>
  - python ProgressiveParty.py -data=<datafile.txt> -parser=ProgressiveParty_Parser.py
  - python ProgressiveParty.py -parser=ProgressiveParty_rally-red.py <number> <number>

## Links
  - https://www.csplib.org/Problems/prob013/
  - https://link.springer.com/article/10.1007/BF00143880
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  recreational, csplib, xcsp23
