""""
Parser for WagInstances at Problem 040 on CSPLib
"""
from pycsp3.problems.data.parsing import *

n, nPeriods = numbers_in(line())
next_line()
children = [[] for _ in range(n)]
for _ in range(n - 1):
    children[next_int()].append(next_int())
nLeaves = len([c for c in children if len(c) == 0])
hcosts = [next_int() for _ in range(n)]
pcosts = [next_int() for _ in range(n)]
demands = [[next_int() for _ in range(nPeriods)] for _ in range(nLeaves)]

data['children'] = children
data['hcosts'] = hcosts
data['pcosts'] = pcosts
data['demands'] = demands



