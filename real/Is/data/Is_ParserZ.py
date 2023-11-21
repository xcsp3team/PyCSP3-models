from pycsp3.problems.data.parsing import *


def read_sets(l):
    return [numbers_in(tok) for tok in l[l.index('{') + 1:l.rindex("}")].split("},{")]


def read_lists(l):
    return [numbers_in(tok) for tok in l[l.index('|') + 1:l.rindex("|")].split("|")]


domSetOfBlockInFunction = read_sets(line())
execFrequencyOfBlockInFunction = numbers_in(next_line())[1:]
defEdgesForBlockInFunction = read_sets(next_line())
data['entryBlockOfFunction'] = number_in(next_line())
funLocDomain = read_lists(next_line())
nBlocks = number_in(next_line())
assert nBlocks == len(domSetOfBlockInFunction) == len(execFrequencyOfBlockInFunction) == len(defEdgesForBlockInFunction)
data['blocks'] = [
    OrderedDict([("domSet", domSetOfBlockInFunction[i]), ("execFrequency", execFrequencyOfBlockInFunction[i]), ("defEdges", defEdgesForBlockInFunction[i])])
    for i in range(nBlocks)]
data['numDataInFunction'] = number_in(next_line())
data['numOperationsInFunction'] = number_in(next_line())
statesInFunction = numbers_in(next_line())
assert len(statesInFunction) == 0
inBlock = read_lists(next_line())
inBlockSucc = read_lists(next_line())
# assert nBlocks == len(data['inBlock']) == len(data['inBlockSucc'])
locDomain = read_lists(next_line().replace("locValueForNull", "-1"))
l = next_line()
applyDefDomUseConstraintForMatch = [1 if tok == "true" else 0 for tok in l[l.index('[') + 1:l.rindex("]")].split(",")]
codeSizeOfMatch = numbers_in(next_line())[1:]
consumedBlocksInMatch = read_sets(next_line())
dataDefinedByMatch = read_sets(next_line())
dataUsedByMatch = read_sets(next_line())
entryBlockOfMatch = read_sets(next_line())
latencyOfMatch = numbers_in(next_line())[1:]
nonCopyMatches = numbers_in(next_line())  # used in MZN for search
operationsCoveredByMatch = read_sets(next_line())
spannedBlocksInMatch = read_sets(next_line())
nLocations = number_in(next_line()) + 1  # +1 for representing the null location
nMatches = number_in(next_line())
assert nMatches == len(applyDefDomUseConstraintForMatch) == len(codeSizeOfMatch) == len(consumedBlocksInMatch) == len(
    dataDefinedByMatch) == len(dataUsedByMatch) == len(entryBlockOfMatch) == len(latencyOfMatch) == len(operationsCoveredByMatch) == len(spannedBlocksInMatch)
data['matches'] = [OrderedDict(
    [("applyDefDomUseConstraint", applyDefDomUseConstraintForMatch[i]), ("codeSize", codeSizeOfMatch[i]), ("consumedBlocks", consumedBlocksInMatch[i]),
     ("dataDefined", dataDefinedByMatch[i]), ("dataUsed", dataUsedByMatch[i]), ("entryBlock", entryBlockOfMatch[i]), ("latency", latencyOfMatch[i]),
     ("operationsCovered", operationsCoveredByMatch[i]), ("spannedBlocks", spannedBlocksInMatch[i])]) for i in range(nMatches)]
# data['nonCopyMatches']  = nonCopyMatches
data['nLocations'] = nLocations
sameLoc = read_lists(next_line())
data['constraints'] = [funLocDomain, inBlock, inBlockSucc, locDomain, sameLoc]
