# Problem SteelMillSlab

Problem 038 on CSPLib.

Steel is produced by casting molten iron into slabs.

## Data
  bench-2-0.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python SteelMillSlab.py -data=<datafile.json>
  python SteelMillSlab.py -data=<datafile.json> -variant=01
```

## Links
  - https://www.csplib.org/Problems/prob038/

## Tags
  realistic, notebook, csplib

<br />

## _Alternative Model(s)_

#### SteelMillSlab_z.py
 - constraints: [BinPacking](http://pycsp.org/documentation/constraints/BinPacking), [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, csplib, mzn17, mzn19
