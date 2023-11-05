from pycsp3.problems.data.parsing import *

from collections import defaultdict

data['n'] = numbers_in(line())[1]
clauses = []
while not line().startswith("solve"):
    if line().startswith("constraint"):
        clauses.append(tuple(number_in(tok) * (-1 if tok[0] == 'n' else 1) for tok in line()[11:-1].split(" \/ ")))
    next_line()
data['clauses'] = clauses
