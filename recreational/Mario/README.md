# Problem Mario

This models a routing problem based on a little example of Mario's day.
Mario is an Italian Plumber and his work is mainly to find gold in the plumbing of all the houses of the neighborhood.
Mario is moving in the city using his kart that has a specified amount of fuel.
Mario starts his day of work from his house and always ends to his friend Luigi's house to have the supper.
The problem here is to plan the best path for Mario in order to earn the more money with the amount of fuel of his kart.

From a more general point of view, the problem is to find a path in a graph:
 - Path endpoints are given (from Mario's to Luigi's)
 - The sum of weights associated to arcs in the path is restricted (fuel consumption)
 - The sum of weights associated to nodes in the path has to be maximized (gold coins)

This problem was proposed by maury Ollagnier and Jean-Guillaume Fages.

## Data Example
  easy-2.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Mario.py -data=<datafile.json>
  python Mario.py -data=<datafile.json> -variant=table
  python Mario.py -data=<datafile.json> -variant=aux
  python Mario.py -data=<datafile.dzn> -parser=Mario_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  recreational

<br />

## _Alternative Model(s)_

#### Mario_z.py
 - constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: recreational, mzn13, mzn14, mzn17
