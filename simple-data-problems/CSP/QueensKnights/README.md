# Problem Quens Knights<span class="csp">CSP</span></h1>

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


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferentMatrix/),
[Intension](https://pycsp.org/documentation/constraints/Intension/).



## Command Line


```shell
python QueensKnights.py
python QueensKnights.py -data=[15,5]
 ```

## Some Results

| Data   | Number of Solutions |
|--------|---------------------|
| \[8,5] | 0                   |
| \[6,6] | 29568               |
