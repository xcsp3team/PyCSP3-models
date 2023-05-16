# Problem De Bruijn Sequence

## Description

You can see below, the beginning of the description provided by [Wolfram Mathworld](https://mathworld.wolfram.com/deBruijnSequence.html):

"*The shortest circular sequence of length $\sigma^n$ such that every string of length $n$ 
on the alphabet $a$ of size $\sigma$ occurs as a contiguous subrange of the sequence described by $a$.*"



### Example

For n=2 and an alphabet (a,b,c), a sequence is 
```
     a a c b b c c a b
```


## Data
a couple \[n,|a|], the value of n and the size of the alphabet. 

## Model(s)



*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/), [Sum](https://pycsp.org/documentation/constraints/Sum/),
[Intension](https://pycsp.org/documentation/constraints/Intension/),
[Cardinality](https://pycsp.org/documentation/constraints/Cardinality/), [Minimum](https://pycsp.org/documentation/constraints/Minimum/)



## Command Line


```shell
python DeBruijnSequence.py
python DeBruijnSequence.py -data=[2,5]
```

## Some Results

| Data   | Number of Solutions |
|--------|---------------------|
| \[2,4] | 16                  |
| \[2,5] | 2048                |
| \[3,2] | 24                  |

