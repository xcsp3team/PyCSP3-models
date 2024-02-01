# Problem PhysicianSchedule

Physician Scheduling During a Pandemic (see link to CPAIOR paper).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Tobias Geibinger, Lucas Kletzander, Matthias Krainz, Florian Mischek, Nysret Musliu and Felix Winter (Copyright 2021).
The licence seems to be like a MIT Licence.

## Data Example
  03-0-34.json

## Model
  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Count](http://pycsp.org/documentation/constraints/Count), [NValues](http://pycsp.org/documentation/constraints/NValues), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python PhysicianSchedule.py -data=sm-10-13-00.json
  python PhysicianSchedule.py -data=sm-10-13-00.dzn -dataparser=PhysicianSchedule_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-78230-6_29
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, mzn21
