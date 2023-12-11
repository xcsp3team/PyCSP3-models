# Problem CookieMonster
## Description
Cookie Monster Problem (by Richard Green)

Suppose that we have a number of cookie jars, each containing a certain number of cookies.
The Cookie Monster (CM) wants to eat all the cookies, but he is required to do so in a number
of sequential moves. At each move, the CM chooses a subset of the jars,
and eats the same (nonzero) number of cookies from each jar. The goal of the CM is to
empty all the cookies from the jars in the smallest possible number of moves, and the
Cookie Monster Problem is to determine this number for any given set of cookie jars.

Concerning data, we need a list of quantities in jars as e.g., [1, 2, 4, 12, 13, 15],
meaning that there are six jars, containing 1, 2, 4, 12, 13 and 15 cookies each.

## Data
  cookies_example.json

## Model
  constraints: [Element](http://pycsp.org/documentation/constraints/Element)

## Execution
  - python CookieMonster.py
  - python CookieMonster.py -data=cookies_example.json

## Links
  - https://bitbucket.org/oscarlib/oscar/src/dev/oscar-cp-examples/src/main/scala/oscar/cp/examples/CookieMonster.scala

## Tags
  academic
