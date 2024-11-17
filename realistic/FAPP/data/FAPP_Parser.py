from pycsp3.problems.data.parsing import *

domains = {}
ln = line()
while ln.startswith("DM"):
    i, v = numbers_in(ln)
    if i not in domains:
        domains[i] = []
    domains[i].append(v)
    ln = next_line()
keys = list(domains.keys())
assert keys == list(range(len(keys)))
data['domains'] = [domains[k] for k in keys]

ln = line()
cnt = 0
routeFrequencies, routePolarizations = [], []
while ln.startswith("TR"):
    i, f, p = numbers_in(ln)
    assert i == cnt and f in keys and p in (-1, 0, 1)
    cnt += 1
    routeFrequencies.append(f)
    routePolarizations.append(p)
    ln = next_line()

data['frequencies'] = routeFrequencies
data['polarizations'] = routePolarizations

hards, softs = [], []
ln = line()
while ln is not None:
    t = ln.split()
    if t[0] == "CI":
        hards.append([int(t[1]), int(t[2]), t[3], t[4], int(t[5])])
    elif t[0] == "CE":
        i, j, eqr = int(t[1]), int(t[2]), [int(v) for v in t[3:]]
        assert len(eqr) == 11
        ln = next_line()
        t = ln.split()
        k, q, ner = int(t[1]), int(t[2]), [int(v) for v in t[3:]]
        assert t[0] == "CD" and i == k and j == q and len(ner) == 11
        softs.append([i, j, eqr, ner])
    ln = next_line()

data['hards'] = hards
data['softs'] = softs
