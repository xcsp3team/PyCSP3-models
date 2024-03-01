# Problem TravelingSalesman

The travelling salesman problem (TSP) asks the following question: "Given a list of cities and the distances between each pair of cities,
what is the shortest possible route that visits each city exactly once and returns to the origin city?" (from wikipedia).

## Data Example
  10-20-0.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python TravelingSalesman.py -data=<datafile.json>
  python TravelingSalesman.py -data=<datafile.json> -variant=table
```

## Links
  - https://en.wikipedia.org/wiki/Travelling_salesman_problem

## Tags
  recreational
