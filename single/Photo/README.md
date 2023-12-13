# Problem Photo
## Description
Betty, Chris, Donald, Fred, Gary, Mary, and Paul want to align in one row for taking a photo.
Some of them have preferences next to whom they want to stand:
 - Betty wants to stand next to Gary and Mary.
 - Chris wants to stand next to Betty and Gary.
 - Fred wants to stand next to Mary and Donald.
 - Paul wants to stand next to Fred and Donald.

## Data
  all integrated (single problem)

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Photo.py
  python Photo.py -variant=aux
```

## Tags
  single
