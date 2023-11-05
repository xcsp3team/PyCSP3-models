from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
nRows = n = number_in(line())
nCols = m = number_in(next_line())
data['nProcessors'] = nRows * nCols
data['nLinks'] = nLinks = number_in(next_line())
nActors = number_in(next_line())
nFlows = number_in(next_line())
data['bandwidth'] = number_in(next_line())
next_line()
data['source_destination_actor'] = [numbers_in(next_line()) for _ in range(nFlows)]
next_line()
actor_processor = [numbers_in(next_line())[0] for _ in range(nActors)]
data['instream'] = numbers_in(next_line(repeat=1))
assert nFlows == len(data['instream'])
next_line(repeat=nFlows)
data['processor_load'] = number_in(next_line())
data['actor_loads'] = numbers_in(next_line())
assert nActors == len(data['actor_loads'])
# data['actors'] = [OrderedDict([("processor", actor_processors[i]), ("load", actor_loads[i])]) for i in range(nActors)]
next_line()
data['arcs'] = [numbers_in(next_line()) for _ in range(nLinks + 2 * n * m)]
