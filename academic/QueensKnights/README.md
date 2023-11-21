# Problem QueensKnights
## Description
This problem is defined in "Boosting systematic search by weighting constraints"
by Boussemart, Hemery, Lecoutre and Sais, ECAI 2004.

The goal is to put m queens in a chess board such that none of the queens can attack each other, and to put n knights such that
all knights form a cycle. Note that the size of the board si n.

### Example
A solution for n=8
![Queens](http://pycsp.org/assets/notebooks/figures/queens.png)

## Data

A couple \[n,m], n is the size of the chess board and n the number of queens.

## Model(s)

  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Intension](http://pycsp.org/documentation/constraints/Intension)



## Command Line

```
python QueensKnights.py
python QueensKnights.py -data=[15,5]
```

## Tags
 academic
