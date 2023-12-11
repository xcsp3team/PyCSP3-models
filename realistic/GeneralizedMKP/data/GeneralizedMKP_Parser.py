from pycsp3.problems.data.parsing import *
from random import seed, shuffle

s = number_in(line())
seed(s)
next_line()
n = next_int()  # number of variables
e = next_int()  # number of constraints
next_line()

data['profits'] = t = [next_int() for _ in range(n)]  # objective coefficients
data['wmatrix'] = [[next_int() for _ in range(n)] for _ in range(e)]
data['capacities'] = [next_int() for _ in range(e)]  # constraint limits

data["pmatrix"] = [t.copy() for _ in range(e)]
for tt in data['pmatrix']:
    shuffle(tt)

assert e == len(data['wmatrix']) == len(data['capacities'])

# python ppycsp3/pproblems/reserve/GeneralizedMKP.py -data=[0,/home/lecoutre/instances/mknap/chubeas/OR5x100/OR5x100-025-1]  -dataparser=ppycsp3/pproblems/reserve/GeneralizedMKP_Parser.py