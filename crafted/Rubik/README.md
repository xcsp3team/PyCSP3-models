# Problem Rubik
## Description
The model, below, is rebuilt from instances submitted to the 2013 Minizinc challenge.
These instances are initially given in flat format (i.e., not from a model).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  execute 'python Rubik.py -data=<datafile.dzn> -parser=Rubik_ParserZ.py -export' for getting JSON files

## Model
  constraints: [Clause](http://pycsp.org/documentation/constraints/Clause)

## Execution
```
  python Rubik.py -data=<datafile.json>
  python Rubik.py -data=<datafile.dzn> -parser=Rubik_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  crafted, mzn13
