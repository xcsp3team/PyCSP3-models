# Problem CommunityDetection17
## Description
The problem is to find communities in a graph with maximum modularity value while satisfying the fact that some pairs of nodes must be assigned
to same or different communities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  strike-s2-k8.json

## Model
  constraints: [Precedence](http://pycsp.org/documentation/constraints/Precedence), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CommunityDetection17.py -data=<datafile.json>
  python CommunityDetection17.py -data=<datafile.dzn> -parser=CommunityDetection17_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-66158-2_31
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  real, mzn17
