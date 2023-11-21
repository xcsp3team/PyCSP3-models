# Problem SetCovering
## Description
Given A set of subsets $S_1,...,S_m$ of the universal set $U=\{1,...,n\}$,
find smallest subset of subsets $T\subset S$ such that $\cup_{t_i \in T} ti=U$.

## Data
The data are represented by a set of subsets S1,...,Sm of the universal set U={1,...,n}.
The problem is to find the smallest number of subsets from S such that their union gives U?

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
    python3 SetCovering.py -data=Subsets_example.json
```


## Links
  -   https://algorist.com/problems/Set_Cover.html

## Tags
recreational
