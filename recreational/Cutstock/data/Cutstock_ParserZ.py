from pycsp3.problems.data.parsing import *

nItems = number_in(line())
capacity = number_in(next_line())
lengths = numbers_in(next_line())
demands = numbers_in(next_line())
assert nItems == len(lengths) == len(demands)
nPieces = sum((demands[i] // (capacity // lengths[i])) + 1 for i in range(nItems))  # very approximate (we must be able to do better)

data["nPieces"] = nPieces
data["pieceLength"] = capacity
data["items"] = [OrderedDict([("length", lengths[i]), ("demand", demands[i])]) for i in range(nItems)]
