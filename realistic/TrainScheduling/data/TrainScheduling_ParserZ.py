from pycsp3.problems.data.parsing import *

STYPE = [TERMINUS, ORDINARY, HUB] = ["TERMINUS", "ORDINARY", "HUB"]
LINE = [SING, DOUB, QUAD, NONE] = ["SING", "DOUB", "QUAD", "NONE"]

ln = line()

STOPS = ln[ln.index('{') + 1:ln.rindex('}')].split(',')
nStops = len(STOPS)
assert STOPS[-1] == "dummy" and all(chr(ord('A') + i) == STOPS[i] for i in range(nStops - 1))
assert next_line() == "dstop = dummy;"

minimal_wait = numbers_in(next_line())
skip_cost = numbers_in(next_line())
platform = numbers_in(next_line())
ln = next_line()
s = ln[ln.index('[') + 1:ln.rindex(']')].split(', ')
stype = [STYPE.index(tok) for tok in s]
next_line()
travel_times = [numbers_in(next_line()) for _ in range(nStops)]
next_line()
lines = [[LINE.index(tok.strip()) for tok in ln[ln.index('|') + 1:].split(', ')] for _ in range(nStops) if (ln := next_line(),)]
assert nStops == len(minimal_wait) == len(skip_cost) == len(platform) == len(stype) == len(travel_times) == len(travel_times[0]) == len(lines) == len(lines[0])
data['stops'] = OrderedDict(
    [("minimal_waits", minimal_wait), ("skip_costs", skip_cost), ("n_platforms", platform), ("types", stype), ("travel_times", travel_times), ("lines", lines)])

next_line()
makespan = number_in(next_line())
min_sep = number_in(next_line())

nRoutes = number_in(next_line())
max_route_length = number_in(next_line())
rlength = numbers_in(next_line())

routes = [[nStops - 1 if tok.strip() == "dstop" else STOPS.index(tok.strip()) for tok in ln[ln.index('|') + 1:].split(', ')] for _ in range(nRoutes) if
          (ln := next_line(),)]
# routes = [routes[i][:rlength[i]] for i in range(nRoutes)]
print(routes)

data['routes'] = routes

ln = next_line(repeat=1)
services = [tok.strip() for tok in ln[ln.index('{') + 1:ln.rindex('}')].split(',')]
nServices = len(services)
service_routes = decrement(numbers_in(next_line()))
service_starts = numbers_in(next_line())
service_ends = numbers_in(next_line())
assert nServices == len(service_routes) == len(service_starts) == len(service_ends)
data['services'] = OrderedDict([("routes", service_routes), ("starts", service_starts), ("ends", service_ends)])

ln = next_line()
engine_names = [tok.strip() for tok in ln[ln.index('{') + 1:ln.rindex('}')].split(',')]
nEngines = len(engine_names)
ln = next_line()
s = ln[ln.index('[') + 1:ln.rindex(']')].split(', ')
start = [STOPS.index(tok) for tok in s]
assert nEngines == len(start)
data['engines'] = OrderedDict([("names", engine_names), ("starts", start)])

data['makespan'] = makespan
data['min_sep'] = min_sep
