# Problem: ChampionsLeague

How many points a team can get while being ranked at a given position?

## Data Example
  2024.json

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python ChampionsLeague.py -data=<datafile.json>
  python ChampionsLeague.py -data=<datafile.json> -variant=strict
  python ChampionsLeague.py -data=[datafile.json,position=number]
  python ChampionsLeague.py -data=[datafile.txt,number] -parser=ChampionsLeague_Parser.py
```

## Links
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
