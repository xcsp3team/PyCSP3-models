from pycsp3.problems.data.parsing import *

nShips = number_in(line())
nTimeSlots = number_in(next_line())
earliest = numbers_in(next_line())
tonnesPerCmDraft = numbers_in(next_line())
nBerthSwaps = number_in(next_line())
berthSwap_incoming = numbers_in(next_line())
berthSwap_outgoing = numbers_in(next_line())
berthSwap_maxTimeDiff = numbers_in(next_line())
assert nBerthSwaps == len(berthSwap_incoming) == len(berthSwap_outgoing) == len(berthSwap_maxTimeDiff)
data['berthSwaps'] = [OrderedDict([("inc", berthSwap_incoming[i]), ("out", berthSwap_outgoing[i]), ("maxTimeDiff", berthSwap_maxTimeDiff[i])]) for i in
                      range(nBerthSwaps)]
next_line()
data['MinSeparationTimeSlots'] = [numbers_in(next_line()) for _ in range(nShips)]
next_line(repeat=1)
data['MaxSailingDraft_cm'] = [numbers_in(next_line()) for _ in range(nTimeSlots)]
data['nTugs'] = number_in(next_line(repeat=1))
maxNTugSets = number_in(next_line())
nTugSetsPerShip = numbers_in(next_line())  # not used
next_line()
tugSetsPerShip = [numbers_in(next_line()) for _ in range(nShips)]
assert all(maxNTugSets == len(row) for row in tugSetsPerShip)
next_line(repeat=1)
tugTurnaroundTimeSlots = [numbers_in(next_line()) for _ in range(nShips)]
IncomingFlag = numbers_in(next_line(repeat=1))  # not used
assert nShips == len(earliest) == len(tonnesPerCmDraft) == len(nTugSetsPerShip) == len(tugSetsPerShip) == len(tugTurnaroundTimeSlots)
data['ships'] = [OrderedDict([("earliest", earliest[i]), ("tonnesPerCmDraft", tonnesPerCmDraft[i]),  # ("nTugSets", nTugSetsPerShip[i]),
                              ("tugSets", tugSetsPerShip[i]), ("tugTurnaroundTimeSlots", tugTurnaroundTimeSlots[i])]) for i in range(nShips)]
data['IncomingShips'] = decrement(numbers_in(next_line()))
data['OutgoingShips'] = decrement(numbers_in(next_line()))
next_line()
data['ExtraTugAllowanceTimeSlots'] = [numbers_in(next_line()) for _ in range(nShips)]
