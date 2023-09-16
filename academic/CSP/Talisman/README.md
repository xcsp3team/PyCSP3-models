
# Problem Talisman

## Description
The definition can be found in [here](https://mathworld.wolfram.com/TalismanSquare.html).

An $n\times n$ array  of the integers from 1 to n<sup>2</sup> such that the difference between any integer
and its neighbor (horizontally, vertically, or diagonally, without wrapping around)
is greater than or equal to some value k is called a (n,k)-talisman square.

### Example
A solution for the (4,2)-talisman square: 

```
      1  8 11 14
      4 16  5  2
     12  9 13 10
     15  6  3  7

```


## Data
A couple \[n,k] defined above.

## Model(s)



*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/),
 [Intension](https://pycsp.org/documentation/constraints/Intension/).


## Command Line


```shell
python Talisman.py
python Talisman.py -data=[5,4]
 ```

## Some Results

| Data   | Number of Solutions |
|--------|---------------------|
| \[3,2] | 0                   |
| \[4,2] | 34714               |
