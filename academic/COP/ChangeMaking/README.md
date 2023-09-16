# Problem Change Making

## Description

The full description can be found in [wikipedia](https://en.wikipedia.org/wiki/Change-making_problem): 

"*The change-making problem addresses the question of finding the minimum number of coins (of certain denominations) that 
add up to a given amount of money. It is a special case of the integer knapsack problem, and has applications wider than 
just currency.*

*It is also the most common variation of the coin change problem, a general case of partition in which, given the 
available denominations of an infinite set of coins, the objective is to find out the number of possible ways 
of making a change for a specific amount of money, without considering the order of the coins.*"

### Example
For n=13, one needs at least 4 coins: 

``` 13 = 3x1 + 10```


## Data
A number n, the given amount of money.

## Model(s)


There are two variants, one classic and one compact (with less variables).


*Involved Constraints*: [Sum](https://pycsp.org/documentation/constraints/Sum/), [Intension](https://pycsp.org/documentation/constraints/Intension/).


## Command Line

```shell
python ChangeMaking.py
python ChangeMaking.py -data=10
python ChangeMaking.py -data=10 -variant=compact
```

## Some Results



| Data                    | Optimum |
|-------------------------|---------|
| 13                      | 4       |
| 28                      | 5       |
| 119                     | 7       |

