# Problem RelToOntology
## Description
The Relational-To-Ontology Mapping Problem is viewed here as a Steiner Tree Problem with side constraints.
See IJCAI paper below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-09.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element)

## Execution
  python RelToOntology.py -data=<datafile.json>
  python RelToOntology.py -data=<datafile.dzn> -parser=RelToOntology_ParserZ.py

## Links
  - https://www.ijcai.org/proceedings/2018/0178.pdf
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  real, mzn17
