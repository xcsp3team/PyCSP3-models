from pycsp3.problems.data.parsing import *

# for DIMACS format

skip_empty_lines(or_prefixed_by="c")
n, e = numbers_in(line())
data['n'] = n
data['e'] = e
data['clauses'] = [numbers_in(next_line())[:-1] for _ in range(e)]
