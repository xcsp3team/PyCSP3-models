# Problem CarSequencing

A number of cars are to be produced; they are not identical, because different options are available as variants on the basic model.
The assembly line has different stations which install the various options (air-conditioning, sunroof, etc.).
These stations have been designed to handle at most a certain percentage of the cars passing along the assembly line.
Furthermore, the cars requiring a certain option must not be bunched together, otherwise the station will not be able to cope.
Consequently, the cars must be arranged in a sequence so that the capacity of each station is never exceeded.
For instance, if a particular station can only cope with at most half of the cars passing along the line, the sequence must
be built so that at most 1 car in any 2 requires that option.

See problem 001 at CSPLib.

## Data Example
  dingbas.json

## Model
  Two variants manage differently the way assembled car options are computed:
  - a main variant involving logical constraints
  - a variant 'table' involving table constraints

  constraints: [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python CarSequencing.py -data=<datafile.json>
  - python CarSequencing.py -data=<datafile.json> -variant=table
  - python CarSequencing.py -data=<datafile.txt> -parser=CarSequencing_Parser.py

## Links
  - https://www.csplib.org/Problems/prob001/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  realistic, csplib, xcsp22
