# Problem: Benzenoide

The benzenoid generation problem is defined as follows: given a set of structural properties P,
generate all the benzenoids which satisfy each property of P.
For instance, these structural properties may deal with the number of carbons, the number of
hexagons or a particular structure for the hexagon graph.
Here, we are interested in generating benzenoids with n hexagons (including benzenoids with ‘holes’).

See the PhD thesis by Adrien Varet (2022, Aix Marseille University).

## Data
  an integer, the order of the coronenoide

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Lex](https://pycsp.org/documentation/constraints/Lex), [Precedence](https://pycsp.org/documentation/constraints/Precedence), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Benzenoide.py -data=number
```

## Links
  - https://www.theses.fr/2022AIXM0508
  - https://link.springer.com/article/10.1007/s10601-022-09328-x
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
