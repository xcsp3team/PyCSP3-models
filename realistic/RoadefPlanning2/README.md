# Problem: RoadefPlanning2

The ROADEF1 conference is the largest French-speaking event aimed at bringing together researchers from various domains, including combinatorial optimization,
 operational research, constraint programming and industrial engineering.
This event is organized annually and welcomes around 600 participants.
ROADEF includes plenary sessions, tutorials in semi-plenary sessions, and multiple parallel sessions.
The conference also involves many working groups consisting of researchers collaborating on a national and potentially international level
 on specific themes covered by the conference, with each parallel session usually being organized by one or more of these working group.
The problem si to schedule ROADEF parallel sessions into available time slots while avoiding clashes among research working groups.


## Data Example
  2021.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python RoadefPlanning2.py -data=<datafile.json>
  python RoadefPlanning2.py -data=[datafile.json,number]
```

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol307-cp2024/LIPIcs.CP.2024.34/LIPIcs.CP.2024.34.pdf
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
