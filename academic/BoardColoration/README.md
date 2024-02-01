# Problem BoardColoration

All squares of a board of a specified size (specified numbers of rows and columns) must be colored with the minimum number of colors.
The four corners of any rectangle inside the board must not be assigned the same color.

### Example
  A solution for 6 rows and 5 columns.
  ```
    0 0 0 0 0
    0 1 1 1 1
    0 1 2 2 2
    1 2 0 1 2
    1 2 0 2 1
    2 2 2 0 1
  ```

## Data
  a pair of numbers: the number of rows (n) and the number of columns (m)

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/COP/BoardColoration/).

  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Maximum](http://pycsp.org/documentation/constraints/Maximum), [NValues](http://pycsp.org/documentation/constraints/NValues)

## Execution
  - python BoardColoration.py -data=[number,number]

## Tags
  academic, notebook
