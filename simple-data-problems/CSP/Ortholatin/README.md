# Problem Ortholatin

## Description
You can see below, the beginning of the description provided by  [wikipedia](https://en.wikipedia.org/wiki/Graeco-Latin_square).

"*A Latin square of order n is an n by n array filled with n different symbols (for example, values between 1 and n),
each occurring exactly once in each row and exactly once in each column.
Two latin squares of the same order n are orthogonal if each pair of elements in the same position occurs exactly once.
The most easy way to see this is by concatenating elements in the same position and verify that no pair appears twice.*"

### Example

A solution for n=5:
```
[0, 1, 2, 3, 4]          [0, 1, 2, 3, 4]
[4, 2, 3, 0, 1]          [3, 4, 1, 2, 0]
[3, 4, 1, 2, 0]          [4, 2, 3, 0, 1]
[1, 3, 0, 4, 2]          [2, 0, 4, 1, 3]
[2, 0, 4, 1, 3]          [1, 3, 0, 4, 2]
```

## Data
A number n, the size of the square.

## Model(s)


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/),
[AllDifferentMatrix](https://pycsp.org/documentation/constraints/AllDifferentMatrix/), [Extension](https://pycsp.org/documentation/constraints/Extension/).



## Command Line


```shell
  python Ortholatin.py
  python Ortholatin.py -data=7
 ```

## Some Results

| Data | Number of Solutions |
|------|---------------------|
| 4    | 2                   |
| 5    | 4                   |
| 6    | 0                   |