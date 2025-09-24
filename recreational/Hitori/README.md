# Problem: Hitori

Hitori

You have to shade some of the cells of a given grid according to the following rules:
 1. No number should appear unshaded more than once in a row or a column.
 2. Two shaded cells cannot be adjacent horizontally or vertically.
 3. All non-shaded cells should be connected in a single group by vertical or horizontal motion.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
For the original mzn model, no Licence was explicitly mentioned (MIT Licence assumed).

Important: this PyCSP3 model is rather different from the mzn model as connectedness is encoded differently.


## Data Example
  h11-1.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Hitori.py -data=<datafile.json>
  python Hitori.py -data=<datafile.dzn> -parser=Hitori_ParserZ.py
```

## Links
  - https://www.puzzle-hitori.com/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  recreational, mzn25
