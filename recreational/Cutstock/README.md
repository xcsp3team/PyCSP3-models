# Problem: Cutstock

Related papers:
 - Mathematical methods of organizing and planning production, L. V. Kantorovich, Management Science, 6(4):366–422, 1960
 - From High-Level Model to Branch-and-Price Solution in G12, J. Puchinger, P. Stuckey, M. Wallace, and S. Brand, CPAIOR 2008: 218-232

## Data Example
  small.json

## Model
  constraints: [Lex](https://pycsp.org/documentation/constraints/Lex), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Cutstock.py -data=<datafile.json>
  python Cutstock.py -data=<datafile.dzn> -parser=Cutstock_ParserZ.py
```

## Links
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
