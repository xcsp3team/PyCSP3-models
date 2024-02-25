from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['n'] = numbers_in(line())[1]
t = numbers_in(next_line())
obj = ([t[i * 2] for i in range(len(t) // 2)], [t[i * 2 + 1] - 1 for i in range(len(t) // 2)])
next_line()
ceq, cge, ciff = [], [], []
while not next_line().startswith("array"):
    t = numbers_in(line())
    op = line()[line().rindex("]") + 2:].split(" ")[0]
    assert op in {'=', '>='}
    if "<->" in line()[:50]:
        assert op == '>='
        ciff.append((t[0] - 1, [t[i * 2 + 1] for i in range(len(t) // 2 - 1)], [t[i * 2 + 2] - 1 for i in range(len(t) // 2 - 1)], t[-1]))
    elif op == '=':
        ceq.append(([t[i * 2] for i in range(len(t) // 2)], [t[i * 2 + 1] - 1 for i in range(len(t) // 2)], t[-1]))
    else:
        cge.append(([t[i * 2] for i in range(len(t) // 2)], [t[i * 2 + 1] - 1 for i in range(len(t) // 2)], t[-1]))
data['eq_constraints'] = ceq
data['ge_constraints'] = cge
data['iff_constraints'] = ciff
data['obj'] = obj
