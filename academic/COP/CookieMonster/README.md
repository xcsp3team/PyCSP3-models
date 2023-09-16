# Problem Cookie Monster

## Description
This problem is proposed by Richard Green

"*Suppose that we have a number of cookie jars, each containing a certain number of cookies.
The Cookie Monster (CM) wants to eat all the cookies, but he is required to do so in a number
of sequential moves. At each move, the CM chooses a subset of the jars,
and eats the same (nonzero) number of cookies from each jar. The goal of the CM is to
empty all the cookies from the jars in the smallest possible number of moves, and the
Cookie Monster Problem is to determine this number for any given set of cookie jars.*"


### Example

The optimum for a grid of size 8 and 4 coins to put in each row and column.

TODO

## Data
We need a list of quantities in jars as e.g., \[1, 2, 4, 12, 13, 15],
meaning that there are six jars, containing 1, 2, 4, 12, 13 and 15 cookies each.

## Model(s)


*Involved Constraints*: [Intension](https://pycsp.org/documentation/constraints/Intension/), [Element](https://pycsp.org/documentation/constraints/Element/).


## Command Line

```shell
python CookieMonster.py
python CookieMonster.py -data=cookies_example.json
```

## Some Results



| Data                    | Optimum |
|-------------------------|---------|
| \[15, 13, 12, 4, 2, 1]  | 4       |
