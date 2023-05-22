# Problem Bacp

## Description
[Problem 30](https://www.csplib.org/Problems/prob030/) of the CSPLib.

The BACP is to design a balanced academic curriculum by assigning periods to courses in a way that the academic load of each period is balanced, i.e., as similar as possible . 

## Data

 - nCourses, nPeriods, minCredits, maxCredits, minCourses, maxCourses 
 - credits (tuple): each course has a number of credits 
 - prerequisites (tuple of tuple): each course has a set of prerequisites

An example is provided in the json file.


## Model
Thera are two variants: 
 - one with extension constraints
 - one with intension constraints (TODO: not sure)

*Involved Constraints*: [Sum](https://pycsp.org/documentation/constraints/Sum) [Intension](https://pycsp.org/documentation/constraints/Intension) [Extension](https://pycsp.org/documentation/constraints/Extension) [Minimum](https://pycsp.org/documentation/constraints/Minimum) [Maximum](https://pycsp.org/documentation/constraints/Maximum) [Count](https://pycsp.org/documentation/constraints/Count)


## Command Line

```shell
python3 Bacp.py -data=TODO [-solve]
```


