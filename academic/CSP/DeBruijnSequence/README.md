# Problem DeBruijnSequence
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

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Intension](http://pycsp.org/documentation/constraints/Intension), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Minimum](http://pycsp.org/documentation/constraints/Minimum)

## Command Line

```
python DeBruijnSequence.py
python DeBruijnSequence.py -data=[2,5]
```

## Tags
 academic
