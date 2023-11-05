from pycsp3.problems.data.parsing import *

data['pixelWidth'] = number_in(line())
data['maxConfig'] = mc = number_in(next_line())
data['n'] = n = number_in(next_line())
data['m'] = m = number_in(next_line())
next_line()
oneline = line() == "-"
if oneline:
    tt = numbers_in(next_line())
    t = [tt[i * mc:i * mc + mc] for i in range(len(tt) // mc)]
else:
    t = [v for _ in range(n * m) for v in numbers_in(next_line())]
data['widths'] = split_with_structure(t, n, m)
if oneline:
    tt = numbers_in(next_line())
    t = [tt[i * mc:i * mc + mc] for i in range(len(tt) // mc)]
else:
    next_line()
    t = [v for _ in range(n * m) for v in numbers_in(next_line())]
data['heights'] = split_with_structure(t, n, m)
