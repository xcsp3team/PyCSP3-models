# Problem AircraftAssemblyLine
## Description
This problem has been proposed by Stéphanie Roussel from ONERA (Toulouse), and comes from an aircraft manufacturer.
The objective is to schedule tasks on an aircraft assembly line in order to minimize the overall number of operators required on the line.
The schedule must satisfy several operational constraints, the main ones being:
- tasks are assigned on a unique workstation (on which specific machines are available);
- the takt-time, i.e. the duration during which the aircraft stays on each workstation, must be respected;
- capacity of aircraft zones in which operators perform the tasks must never be exceeded;
- zones can be neutralized by some tasks, i.e. it is not possible to work in those zones during the tasks execution.

This model has been co-developed by teams of ONERA and CRIL.

## Data (example)
  1-178-00-0.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python AircraftAssemblyLine.py -data=<datafile.json> -dataParser=AircraftAssemblyLine_Converter.py
```

## Links
  - https://drops.dagstuhl.de/opus/frontdoor.php?source_opus=19069
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, xcsp23
