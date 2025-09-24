# Problem: WorkTaskVariation

Work Task Variation problem (WTV)

From CP'25 paper (cited below) Given a schedule with fixed worker time slots and task assignments, the core challenge of the WTV problem
lies in rearranging tasks between workers while preserving the original time slot allocations to improve flow and ergonomics.
The cost function penalizes both excessively short and long spans of a single task, aiming for a balanced variety minimizing repetitive strain
and promotes engagement.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
The original mzn model by Mikael Zayenz Lagerkvist and Magnus Rattfeldt -- No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  s03-l10-o08-w12-b15.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Element](https://pycsp.org/documentation/constraints/Element), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python WorkTaskVariation.py -data=<datafile.json>
  python WorkTaskVariation.py -data=<datafile.dzn> -parser=WorkTaskVariation_ParserZ.py
```

## Links
  - https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.24
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
