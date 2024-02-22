# Problem Vellino

From "Constraint Programming in OPL", P. Van Hentenryck, L. Michel, L. Perron, and J.-C. Régin, CP'99

This configuration problem involves putting components of different materials (glass, plastic, steel, wood, and copper)
into bins of various types/colors (red, blue, green), subject to capacity (each bin type has a maximum capacity) and compatibility constraints.
Every component must be placed into a bin and the total number of used bins must be minimized.
The compatibility constraints are:
 - red bins cannot contain plastic or steel
 - blue bins cannot contain wood or plastic
 - green bins cannot contain steel or glass
 - red bins contain at most one wooden component
 - green bins contain at most two wooden components
 - wood requires plastic
 - glass excludes copper
 - copper excludes plastic

## Data Example
  05.json

## Model
  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Vellino.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/chapter/10.1007/10704567_6

## Tags
  recreational, notebook

<br />

## _Alternative Model(s)_

#### Vellino2.py
 - constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: recreational, notebook
