
# Problem Quasigroup

## Description
This is the [problem 003](https://www.csplib.org/Problems/prob003/) of the CSPLib:

"*An order m quasigroup is a Latin square of size m. That is, a m×m multiplication table in which each element occurs once in every row and column.:*"


### Example

```
1    2   3   4
4    1   2   3
3    4   1   2
2    3   4   1
```

## Data
A number n, the size of the square.
## Model(s)

There are 7 variants of this problem.



You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Quasigroup/).


*Involved Constraints*: [AllDifferentMatrix](https://pycsp.org/documentation/constraints/AllDifferentMatrix/),
[Element](https://pycsp.org/documentation/constraints/Element/).



## Command Line


```shell
python QuasiGroup.py
python QuasiGroup.py -data=8 -variant=base-v3
python QuasiGroup.py -data=5 -variant=base-v4
python QuasiGroup.py -data=8 -variant=base-v5
python QuasiGroup.py -data=8 -variant=base-v6
python QuasiGroup.py -data=9 -variant=base-v7
python QuasiGroup.py -data=8 -variant=aux-v3
python QuasiGroup.py -data=5 -variant=aux-v4
python QuasiGroup.py -data=8 -variant=aux-v5
python QuasiGroup.py -data=9 -variant=aux-v7
 
 ```

## Some Results
These are results without variant

| Data | Number of Solutions |
|------|---------------------|
| 4    | 2                   |
| 5    | 48                  |
| 6    | 10752               |
