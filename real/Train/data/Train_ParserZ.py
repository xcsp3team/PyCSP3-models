from pycsp3.problems.data.parsing import *

n = number_in(line())
m = number_in(next_line())
data['maxTime'] = number_in(next_line())
delayTime = number_in(next_line())
delayTrain = number_in(next_line()) - 1
delayDuration = number_in(next_line())
data['delay'] = OrderedDict([("time", delayTime), ("train", delayTrain), ("duration", delayDuration)])

distances = numbers_in(next_line()) + [-1]  # -1 for the last (irrelevant) distance
passengerStarts = numbers_in(next_line())
passengerFlows = numbers_in(next_line())
assert m == len(passengerStarts) == len(passengerFlows) == len(distances)
data['stations'] = [OrderedDict([("passengerStart", passengerStarts[i]), ("passengerFlow", passengerFlows[i]), ("distance", distances[i])])
                    for i in range(m)]

scheduledArrivals = split_with_rows_of_size(numbers_in_lines_until(";"), m)
scheduledDepartures = split_with_rows_of_size(numbers_in_lines_until(";"), m)
assert n == len(scheduledArrivals) == len(scheduledDepartures)
data['trains'] = [OrderedDict([("scheduledArrival", scheduledArrivals[i]), ("scheduledDeparture", scheduledDepartures[i])]) for i in range(n)]

data['capacity'] = number_in(next_line())
