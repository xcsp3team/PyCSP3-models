from pycsp3.problems.data.parsing import *

nItems = number_in(line())
capacity = number_in(next_line())
m = [numbers_in(next_line()) for _ in range(nItems)]
nPieces = sum((t[1] // (capacity // t[0])) + 1 for t in m)  # very approximate (we must be able to do better)

data["nPieces"] = nPieces
data["pieceLength"] = capacity
data["items"] = [OrderedDict([("length", t[0]), ("demand", t[1])]) for t in m]
