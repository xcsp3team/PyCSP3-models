# Problem TravelingTournament

The Traveling Tournament Problem is a sports timetabling problem that abstracts two issues in creating timetables:
home/away pattern feasibility and team travel (from link below).

## Data Example
  galaxy04.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Regular](http://pycsp.org/documentation/constraints/Regular), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python TravelingTournament.py -data=<datafile.json> -variant=a2
  python TravelingTournament.py -data=<datafile.json> -variant=a3
```

## Links
  - https://www.researchgate.net/publication/220270875_The_Traveling_Tournament_Problem_Description_and_Benchmarks

## Tags
  recreational, notebook
