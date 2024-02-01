# Problem RIP

The Resource Investment Problem (RIP) is also known as the Resource Availability Cost Problem (RACP).
The RIP assumes that the level of renewable resources can be varied at a certain cost and aims at minimizing this total cost
of the (unlimited) renewable resources required to complete the project by a pre-specified project deadline.


## Data (example)
  25-0-j060-01-01.json

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python RIP.py -data=<datafile.json>
  - python RIP.py -data=<datafile.txt> -parser=RIP_Parser.py

## Links
  - https://www.projectmanagement.ugent.be/research/project_scheduling/racp
  - https://ideas.repec.org/a/eee/ejores/v266y2018i2p472-486.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
