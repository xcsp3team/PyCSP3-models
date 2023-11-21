from pycsp3.problems.data.parsing import *
# from random import randrange, seed

k = number_in(line())
# d = number_in(next_line())
# s = number_in(next_line())
# seed(s)
next_line()
skip_empty_lines(or_prefixed_by="#")
t = [numbers_in(l) for l in remaining_lines()]
n = t[-1][0] + 1
m = [[-1] * n for _ in range(n)]
for i, j, w, p in t:
    assert p == 0
    m[i-1][j-1] = 0 if i == j else w  #randrange(1, d)
data['weights'] = m
data["k"] = k

# python ppycsp3/pproblems/mzn19/KidneyExchange.py -data=[4,100,0,/home/lecoutre/instances/kidneyExchangeProgramme/instances/071] -dataparser=ppycsp3/pproblems/mzn19/KidneyExchange_ParserW.py  -ev
# python ppycsp3/pproblems/mzn19/KidneyExchange.py -data=[4,/home/lecoutre/instances/kidneyExchangeProgramme/instances/061] -dataparser=ppycsp3/pproblems/mzn19/KidneyExchange_ParserW.py  -ev -dataexport