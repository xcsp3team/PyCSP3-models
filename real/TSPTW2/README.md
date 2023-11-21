# Problem TSPTW2
## Description
The Traveling Salesman Problem with Time Windows (TSPTW) is a popular variant of the TSP where the salesman’s customers
must be visited within given time windows.
See IJCAI paper below.

## Data (example)
  n020w020-1.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python TSPTW2.py -data=<datafile.json>
  - python TSPTW2.py -data=<datafile.txt> -parser=TSPTW_Parser.py

## Links
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, xcsp23
