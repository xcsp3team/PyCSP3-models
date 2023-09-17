# Problem CryptoPuzzle
## Description

You can see below, the beginning of the description provided by [wikipedia](https://en.wikipedia.org/wiki/Verbal_arithmetic):

"*Verbal arithmetic, also known as alphametics, cryptarithmetic, cryptarithm or word addition, is a type of
mathematical game consisting of a mathematical equation among unknown numbers, whose digits are represented by letters of the alphabet.*"


### Example

For the Puzzle:
```
    S E N D
+   M O R E
= M O N E Y
```
a possible solution is:

```
    9 5 6 7
+   1 0 8 5
= 1 0 6 5 2
```

## Data
A list contaning three words: \[send,more,money\] for example

## Model(s)

There are a main variant and a variant with carry variables.

You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/CryptoPuzzle/).


  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Intension](http://pycsp.org/documentation/constraints/Intension)


## Command Line

```
python CryptoPuzzle.py -data=[send,more,money]
python CryptoPuzzle.py -data=[send,more,money] -variant=carry
```

## Tags
 academic
