# Problem: CommunityDetection

Constrained Community Detection Problem

The problem is to find communities in a graph with maximum modularity value while satisfying the fact that some pairs of nodes must be assigned
to same or different communities.
See CP paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n050-e2500-s10-d5-c4-p90.json

## Model
  constraints: [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python CommunityDetection.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-66158-2_31
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, notebook, mzn21

<br />

## _Alternative Model(s)_

#### CommunityDetection_z1.py
 - constraints: [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Sum](https://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, mzn17, mzn24
