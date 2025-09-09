# Problem: TrainSchedule

The Brussels Central Problem (Fom course at UCL -- Louvain La Neuve)

The SNCB finally decided to rely on optimization technologies to schedule the departure
of its fleet at Brussels central. The problem to be solved is the following:
- Each train has a scheduled departure time.
- If a train departs earlier or later than expected, a penalty cost is incurred per time unit.
- After a train has left the station, no other train can depart for a given period
 (number of time units, or 'gap', which depends upon the train that has left).
- The goal is to minimize the cost incurred by early and late departs.

## Data Example
  Brussels.json

## Model
  constraints: [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TrainSchedule.py -data=<datafile.json>
```

## Tags
  recreational
