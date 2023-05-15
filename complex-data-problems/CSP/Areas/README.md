# Problem Areas

## Description


A rectangular board is given with some squares specified as positive integers.
Fill in all squares of the board with positive integers so that any maximal contiguous set of squares containing the same integer
has the area equal to this integer (two squares are contiguous if they share a side).

The Areas Problem is fully described in this [paper](https://www.researchgate.net/publication/221090944_Teaching_Constraints_through_Logic_Puzzles); 
See Figure 1. 


## Data
Data can be found in the archive. It contains 2 JSON files. Each instance is defined by a JSON object with 1 main field (puzzle).

*Data files are welcome!*


## Model

*Involved Constraints*: [Intension](https://pycsp.org/documentation/constraints/Intension/), [Extension](https://pycsp.org/documentation/constraints/Extension/), [Count](https://pycsp.org/documentation/constraints/Count/)



## Command Line

```shell
python3 Areas.py -data=Areas-3-3-3.json [-solve]
```

## Some Results

| Data | Number of Solutions
| ---  | ---          
| Areas-3-3-3.json   | 7
| Areas-5-5-9.json   | 1


