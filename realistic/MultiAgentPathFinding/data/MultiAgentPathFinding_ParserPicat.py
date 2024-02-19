from pycsp3.problems.data.parsing import *

next_line()
M = []
l = next_line().strip()
while l[0] != 'A':
    M.append(numbers_in(l))
    l = next_line().strip()
n = len(M)

data['agents'] = decrement(split_with_rows_of_size(numbers_in(line()), 2))


def coordinates(v):
    return next((i, j) for i in range(n) for j in range(n) if M[i][j] == v)


def distance(v1, v2):
    (i1, j1), (i2, j2) = coordinates(v1), coordinates(v2)
    return abs(i1 - i2) + abs(j1 - j2)


data['horizon'] = sum(distance(v1, v2) for v1, v2 in data['agents'])


def neighbors_of(v):
    i, j = coordinates(v)
    return [v] + [M[k][l] for k, l in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if 0 <= k < n and 0 <= l < n and M[k][l] != 0]


data['neighbors'] = decrement([neighbors_of(v) for v in range(1, max(v for row in M for v in row) + 1)])
