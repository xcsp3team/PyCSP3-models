"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  p-d02.json

## Model
  constraints: Element, Maximum, NoOverlap

## Execution
  python PillarsPlanks.py -data=<datafile.json>
  python PillarsPlanks.py -data=<datafile.dzn> -parser=PillarsPlanks_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

plankWidths, pillarHeights, pillarWidths, width, height = data
nPlanks, nPillars = len(plankWidths), len(pillarHeights)

plankWidthsx = cp_array(plankWidths + [width])

# xk[i] is the x-coordinate of the ith plank
xk = VarArray(size=nPlanks, dom=range(width))

# yk[i] is the y-coordinate of the ith plank
yk = VarArray(size=nPlanks, dom=range(height))

# xr[i] is the x-coordinate of the ith pillar
xr = VarArray(size=nPillars, dom=range(width))

# yr[i] is the y-coordinate of the ith pillar
yr = VarArray(size=nPillars, dom=range(height))

# left[i] is the pillar supporting the ith plank on the left
left = VarArray(size=nPlanks, dom=range(nPillars))

# right[i] is the pillar supporting the ith plank on the right
right = VarArray(size=nPlanks, dom=range(nPillars))

# support[j] is the plank where is sit the jth pillar (or nPlanks if none)
support = VarArray(size=nPillars, dom=range(nPlanks + 1))

xka = Var(0)
yka = Var(-1)

# two auxiliary arrays
xkx, ykx = cp_array(xk + [xka]), cp_array(yk + [yka])

satisfy(
    # ensuring that the structure stays within the allocated space
    [
        [xk[p] + plankWidths[p] <= width for p in range(nPlanks)],
        [xr[p] + pillarWidths[p] <= width for p in range(nPillars)],
        [yr[p] + pillarHeights[p] <= height for p in range(nPillars)]
    ],

    # tag(symmetry-breaking)
    (
        [
            If(
                yk[p1] <= yk[p2], yk[p1] == yk[p2],
                Then=xk[p1] < xk[p2]
            ) for p1, p2 in combinations(nPlanks, 2) if plankWidths[p1] == plankWidths[p2]
        ],
        [
            If(
                yr[p1] <= yr[p2], yr[p1] == yr[p2],
                Then=xr[p1] < xr[p2]
            ) for p1, p2 in combinations(nPillars, 2) if pillarWidths[p1] == pillarWidths[p2] and pillarHeights[p1] == pillarHeights[p2]
        ],
    ),

    NoOverlap(
        origins=(xk + xr, yk + yr),
        lengths=(plankWidths + pillarWidths, [1] * nPlanks + pillarHeights)
    ),

    # each plank is supported at both ends by a pillar
    (
        (
            xr[left[p]] <= xk[p],
            xr[left[p]] + pillarWidths[left[p]] > xk[p],
            yk[p] == yr[left[p]] + pillarHeights[left[p]],
            xr[right[p]] <= xk[p] + plankWidths[p] - 1,
            xr[right[p]] + pillarWidths[right[p]] > xk[p] + plankWidths[p] - 1,
            yk[p] == yr[right[p]] + pillarHeights[right[p]]
        ) for p in range(nPlanks)
    ),

    # each pillar sits on exactly one plank
    (
        (
            xr[p] >= xkx[support[p]],
            xr[p] + pillarWidths[p] <= xkx[support[p]] + plankWidthsx[support[p]],
            yr[p] == ykx[support[p]] + 1
        ) for p in range(nPillars)
    )
)

minimize(
    # minimizing the height of the structure
    Maximum([yk[p] + 1 for p in range(nPlanks)] + [yr[p] + pillarHeights[p] for p in range(nPillars)])
)

"""
(support[p] == -1) | (yr[p] == ykx[support[p]]) est ok 
 mais (support[p] == -1) | (yr[p] == ykx[support[p]] + 1) non. Why?
"""
