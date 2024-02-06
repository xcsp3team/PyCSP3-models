# Problem Sugiyama

Optimal ordering layout for a Sugiyami style graph.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  g3-8-8-2.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Sugiyama.py -data=<datafile.json>
  python Sugiyama.py -data=<datafile.dzn> -parser=Sugiyama_ParserZ.py
```

## Links
  - https://en.wikipedia.org/wiki/Layered_graph_drawing
  - https://www.minizinc.org/challenge2010/results2010.html

## Tags
  crafted, mzn10
