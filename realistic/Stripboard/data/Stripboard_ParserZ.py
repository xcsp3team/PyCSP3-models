from pycsp3.problems.data.parsing import *

orientations = ["Upright", "Clockwise", "UpsideDown", "Anticlockwise"]

data['maxw'] = number_in(line())
data['maxh'] = number_in(next_line())
data['max_links'] = number_in(next_line())
l = next_line()
components = l[l.index('{') + 1:l.rindex('}')].split(', ')
next_line()
allowed_orientations = []
for s in components:
    l = next_line()
    assert l.startswith(s)
    allowed_orientations.append(orientations if l.endswith('ORIENTATION,') else l[l.index('{') + 1:l.rindex('}')].split(', '))
# data['allowed_orientations'] = allowed_orientations
next_line(repeat=1)
pins = [next_line()[:-1].strip().split(', ') for _ in range(len(components))]
next_line()
l = next_line()
nets = l[l.index('{') + 1:l.rindex('}')].split(', ')
l = next_line()
footprint_w = [p.split(": ") for p in l[l.index('[') + 1:l.rindex(']')].split(', ')]
assert all(components[i] == s for i, (s, v) in enumerate(footprint_w))
l = next_line()
footprint_h = [p.split(": ") for p in l[l.index('[') + 1:l.rindex(']')].split(', ')]
assert all(components[i] == s for i, (s, v) in enumerate(footprint_h))
data['components'] = [(s, int(footprint_w[i][1]), int(footprint_h[i][1]), allowed_orientations[i]) for i, s in enumerate(components)]
next_line()
pins_dx = []
for i in range(len(components)):
    tt = [p.split(": ") for p in next_line().strip()[:-1].split(', ')]
    assert all(pins[i][j] == tt[j][0] for j in range(len(pins[i])))
    pins_dx.append(tt)
next_line(repeat=1)
pins_dy = []
for i in range(len(components)):
    tt = [p.split(": ") for p in next_line().strip()[:-1].split(', ')]
    assert all(pins[i][j] == tt[j][0] for j in range(len(pins[i])))
    pins_dy.append(tt)
next_line(repeat=1)
pins_net = []
for i in range(len(components)):
    tt = [p.split(": ") for p in next_line().strip()[:-1].split(', ')]
    assert all(pins[i][j] == tt[j][0] for j in range(len(pins[i])))
    pins_net.append(tt)
data['pins'] = [[(s, int(pins_dx[i][j][1]), int(pins_dy[i][j][1]), pins_net[i][j][1]) for j, s in enumerate(t)] for i, t in enumerate(pins)]
data['nets'] = nets
