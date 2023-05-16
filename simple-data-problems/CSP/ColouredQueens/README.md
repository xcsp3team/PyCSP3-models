# Problem Coloured Queens

## Description


The queens graph is a graph with n*n nodes corresponding to the squares of a chess-board.
There is an edge between nodes iff they are on the same row, column, or diagonal, i.e. if two queens on those squares would attack each other.
The coloring problem is to color the queens graph with n colors.
See Tom Kelsey, Steve Linton, Colva M. Roney-Dougal: [New Developments in Symmetry Breaking in Search Using Computational Group Theory](https://link.springer.com/chapter/10.1007/978-3-540-30210-0_17). AISC 2004: 199-210.


### Example

An example of a solution for n=7 is:
```
     4 5 3 1 2 0 6
     0 6 4 5 3 1 2
     1 2 0 6 4 5 3
     5 3 1 2 0 6 4
     6 4 5 3 1 2 0
     2 0 6 4 5 3 1
     3 1 2 0 6 4 5
```

## Data
a number n, the size of the chessboard.


## Model(s)


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/). 


## Command Line

```shell
python ColouredQueens.py
python ColouredQueens.py -data=10
```

## Some Results

| Data | Number of Solutions
| --- | ---          
| 6   | 0
| 7   | 20160
