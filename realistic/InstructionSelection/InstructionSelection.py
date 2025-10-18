"""
Universal Instruction Selection.

Processors are built to execute a vast range of programs.
Techniques for instruction selection – the task of choosing the instructions for a given program – have not been so well studied.
This is the case in the PhD thesis of Gabriel Hjort Blindell in 2018,
with an approach that combines instruction selection with global code motion and block ordering.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2020/2025 Minizinc challenges.
The original MZN model was proposed by Gabriel Hjort Blindell (Copyright (c) 2013-2015)

## Data Example
  A3PZaPjnUz.json

## Model
  constraints: Circuit, Count, Sum, Table

## Execution
  python InstructionSelection.py -data=<datafile.json>
  python InstructionSelection.py -data=<datafile.dzn> -parser=InstructionSelection_ParserZ.py

## Links
  - https://www.semanticscholar.org/paper/Universal-Instruction-Selection-Blindell/79f97178fb5493e0a1fe32073773de19faf22868
  - https://link.springer.com/chapter/10.1007/978-3-319-23219-5_42
  - https://link.springer.com/book/10.1007/978-3-319-34019-7
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn15, mzn20, mzn25
"""

from pycsp3 import *

entryBlockOfFunction, blocks, nData, nOperations, matches, nLocations, constraints = data or load_json_data("A3PZaPjnUz.json")

funLocDomain, inBlock, inBlockSucc, locDomain, sameLoc = constraints
nBlocks, nMatches = len(blocks), len(matches)

statesInFunction = []  # checked in the parser
execFrequencies = cp_array([block.execFrequency for block in blocks] + [0])  # we add 0 ; we need cp_array for a constraint Element


def is_dominated(i2, m2):
    excluded = set(sameLoc[:, 0]) | set(inBlock[:, 0]) | set(inBlockSucc[:, 0])
    for i1, m1 in enumerate(matches):
        if i1 == i2 or i1 in excluded or i2 in excluded:
            continue
        if not ((m1.latency < m2.latency) or (m1.latency == m2.latency and i1 < i2)):
            continue
        if m1.operationsCovered != m2.operationsCovered or m1.dataDefined != m2.dataDefined:
            continue
        if m1.dataUsed != m2.dataUsed or m1.entryBlock != m2.entryBlock:
            continue
        if m1.spannedBlocks != m2.spannedBlocks or m1.applyDefDomUseConstraint != m2.applyDefDomUseConstraint:
            continue
        possible = True
        for i, li in enumerate(locDomain):
            if li[0] == i1:
                found = False
                for j, lj in enumerate(locDomain):
                    if lj[0] == i2 and lj[1] == li[1]:
                        if li[2] <= lj[2] and lj[3] <= li[3]:
                            found = True
                            break
                if not found:
                    possible = False
                    break
        if possible:
            return True
    return False


dominated = [i for i in range(nMatches) if is_dominated(i, matches[i])]
non_dominated = [i for i in range(nMatches) if i not in dominated]

# for Ad hoc: detect symmetry among location values 1..31
possible_early_symmetry = (all(lo > 31 or hi >= 31 or hi == 0 for _, lo, hi in funLocDomain) and
                           all(lo > 31 or hi >= 31 or hi == 0 for _, _, lo, hi in locDomain))

T = [(i, j) for i in range(nBlocks) for j in blocks[i].domSet] + [(nBlocks, v) for v in range(nBlocks)]

# x[i] is the block (definition) of the ith datum
x = VarArray(size=nData, dom=range(nBlocks))

# y[i] is the location of the ith datum
y = VarArray(size=nData, dom=range(nLocations))

# sl[m] is 1 if the match m is selected
sl = VarArray(size=nMatches, dom={0, 1})

# pl[m] is the block where is placed the match m
pl = VarArray(size=nMatches, dom=range(nBlocks + 1))

# succ[b] is the block succeeding to block b in the generated code
succ = VarArray(size=nBlocks + 1, dom=range(nBlocks + 1))

satisfy(
    # enforcing that, for each operation, exactly one match must be selected such that the operation is covered
    [(sl[t[0]] ^ sl[t[1]]) if len(t) == 2 else ExactlyOne(sl[t])
     for t in [[m for m in non_dominated if o in matches[m].operationsCovered] for o in range(nOperations)]],

    # enforcing that, for each datum, exactly one match must be selected such that the datum is defined
    [(sl[t[0]] ^ sl[t[1]]) if len(t) == 2 else ExactlyOne(sl[t])
     for t in [[m for m in non_dominated if e in matches[m].dataDefined] for e in range(nData)]],

    # the total number of data defined by the selected matches must be equal to the number of data in the function graph  tag(redundant)
    Sum(len(matches[m].dataDefined) * sl[m] for m in non_dominated) == nData,

    # selected matches must not be placed in the null bloc
    [sl[m] == (pl[m] != nBlocks) for m in range(nMatches)],

    # selected matches that have an entry block must be placed in entry block
    [pl[m] in {b, nBlocks} for m in non_dominated for b in matches[m].entryBlock],

    # a datum defined by a selected match must be defined in either the block wherein the match is placed or in one of the blocks spanned by the match
    [
        If(
            sl[m],
            Then=(x[i] in matches[m].spannedBlocks) if len(matches[m].spannedBlocks) > 0 else (x[i] == pl[m])
        ) for m in non_dominated for i in matches[m].dataDefined
    ],

    # no selected matches may be placed in a block which is consumed by some selected match
    [
        If(
            sl[m1],
            Then=pl[m2] != b
        ) for m1 in range(nMatches) for m2 in range(nMatches) for b in matches[m1].consumedBlocks
    ],

    # For every block wherein a datum is defined, there must exist some selected match such that it is either placed in that block
    # or that block is part of one of the blocks that appear in the selected match
    [
        If(
            x[i] == b,
            Then=Exist(pl[m] == b if b not in matches[m].spannedBlocks else either(pl[m] == b, sl[m]) for m in non_dominated)
        ) for i in range(nData) for b in range(nBlocks)
    ],

    # a datum with a definition edge with a block must be defined in the block of that block
    [x[i] == b for b in range(nBlocks) for i in blocks[b].defEdges],

    # enforcing that every datum is defined in a block such that the block dominates all blocks wherein the datum is used
    [(pl[m], x[i]) in T for m in non_dominated for i in matches[m].dataUsed if matches[m].applyDefDomUseConstraint == 1],

    # ensuring a circuit (thus resulting in an ordering of blocks)
    Circuit(succ),

    # placing the block of the entry block as the first block
    succ[-1] == entryBlockOfFunction,

    # constraining the location for all data that are states
    [y[i] == nLocations - 1 for i in statesInFunction],

    # parameterized constraints
    [
        [
            If(
                sl[m],
                Then=y[p] == y[q]
            ) for m, p, q in sameLoc
        ],
        [
            both(
                pl[m] in {p, nBlocks},
                If(sl[m], Then=succ[p] == q)
            ) for m, p, q in inBlockSucc
        ],
        [pl[m] in {p, nBlocks} for m, p in inBlock],
        [
            If(
                sl[m],
                Then=y[l] in range(mi, ma + 1)
            ) for m, l, mi, ma in locDomain if mi != -1 and ma != -1
        ],
        [y[i] in range(mi, ma + 1) for i, mi, ma in funLocDomain]
    ],

    # tag(redundant)
    [
        # forbidding two matches to be selected together if they imply conflicting successor blocks
        [
            either(
                sl[mi] == 0,
                sl[mj] == 0
            ) for i, (mi, pi, qi) in enumerate(inBlockSucc) for j, (mj, pj, qj) in enumerate(inBlockSucc) if i < j and (pi == pj) ^ (qi == qj)
        ],

        # forbidding two matches to be selected together if the first implies that two locations are equal
        # and the second implies that the intersection of their domains is empty
        [
            either(
                sl[m] == 0,
                sl[m2] == 0
            ) for m, p, q in sameLoc for m1, l1, mi1, ma1 in locDomain if l1 == p for m2, l2, mi2, ma2 in locDomain
            if m1 == m2 and l2 == q and (ma1 < mi2 or ma2 < mi1)
        ]
    ],

    # possible detection of symmetry among location values 1..31
    [y[i] not in range(1, 31) for i in range(nData)] if possible_early_symmetry else None,

    # dominated matches cannot be selected
    [sl[m] == 0 for m in dominated]
)

minimize(
    Sum(matches[m].latency * execFrequencies[pl[m]] for m in non_dominated)
)

""" Comments
1) it would be reasonable to decompose:
 [belong(pl[m], {p, nBlocks}) & If(sl[m], Then=succ[p] == q) for m, p, q in inBlockSucc],

2)
  x == [0, 0, 2, 2, 4, 0, 4, 0, 5, 6, 0, 6, 7, 0, 0, 0, 0, 1, 2, 2, 0, 2, 3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 7, 0, 0],
  y == [31, 34, 31, 34, 31, 0, 31, 0, 33, 31, 0, 31, 31, 31, 31, 0, 0, 31, 31, 31, 31, 0, 31, 31, 31, 31, 0, 31, 31, 31, 0, 31, 31, 31, 31, 0, 0],
  sl == [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0,
          1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
3) {0}.union(set(range(31, nLocations))
"""
