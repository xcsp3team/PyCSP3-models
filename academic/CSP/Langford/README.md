# Problem Langford

## Description
This is the [problem 024](https://www.csplib.org/Problems/prob024/) of the CSPLib:

"*Consider two sets of the numbers from 1 to 4. The problem is to arrange the eight numbers in the two sets into 
a single sequence in which the two 1’s appear one number apart, the two 2’s appear two numbers apart, the two 3’s 
appear three numbers apart, and the two 4’s appear four numbers apart.*"

### Example
A graphical representation of L(2,4) with  with black=1, red=2, blue=3 and yellow=4 (source CSPLib)

![langford](https://www.csplib.org/Problems/prob024/assets/langford.gif)

## Data
A couple \[k,n\], n is the number of values and k the number of occurences for a value.
## Model(s)


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/), [Intension](https://pycsp.org/documentation/constraints/Intension/).



## Command Line


```shell
  python Langford.py
  python Langford.py -data=[3,10]
 ```

## Some Results

| Data    | Number of Solutions |
|---------|---------------------|
| \[2,4]  | 2                   |
| \[3,10] | 10                  |
| \[4,12] | 0                   |
