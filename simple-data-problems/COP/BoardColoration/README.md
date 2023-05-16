# Problem Board Coloration

## Description
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
A couple \[n,m], n is the number of rows and m the number of columns.

## Model(s)


There are 3 variants according to  the way optimization must be conducted (called card, span, max).

You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/COP/BoardColoration/).


*Involved Constraints*: [NValues](https://pycsp.org/documentation/constraints/NValues/), [Maximum](https://pycsp.org/documentation/constraints/Maximum/), 
[LexIncreasing](https://pycsp.org/documentation/constraints/LexIncreasing/).



## Command Line

```shell
python BoardColoration.py
python BoardColoration.py -data=[8,10]
```

## Some Results



| Data                    | Optimum |
|-------------------------|---------|
| \[6,5]                  | 2       |
| \[8,10]                 | 2       |

