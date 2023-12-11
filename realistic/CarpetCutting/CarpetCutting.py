"""
The carpet cutting problem is a two-dimensional cutting and packing problem in which carpet shapes are cut
from a rectangular carpet roll with a fixed roll width and a sufficiently long roll length.
See the "Optimal Carpet Cutting" conference paper published at CP'11.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  test01.json

## Model
  constraints: Cumulative, NoOverlap, Sum, Table

## Execution
  python CarpetCutting.py -data=test01.json

## Links
  - https://link.springer.com/chapter/10.1007/978-3-642-23786-7_8
  - https://www.minizinc.org/challenge2021/results2021.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, mzn11, mzn12, mzn16, mzn21, xcsp23
"""

from pycsp3 import *

rollWidth, maxRollLength, roomCarpets, rectangles, stairCarpets = data
roomRectangles, possibleRotations, maxLengths, maxWidths = zip(*roomCarpets)
rectLengths, rectWidths, xOffsets, yOffsets = zip(*rectangles)
stairLengths, stairWidths, nCoveredSteps, minCutSteps, maxCuts = zip(*stairCarpets) if len(stairCarpets) > 0 else ([], [], [], [], [])
nRoomCarpets, nRectangles, nStairCarpets = len(roomCarpets), len(rectangles), len(stairCarpets)

RC, SC = range(nRoomCarpets), range(nStairCarpets)

R0, R90, R180, R270 = Rotations = range(4)  # 0 - 0, 1 - 90, 2 - 180, and 3 - 270

stairOffsets = [sum(nCoveredSteps[:i]) for i in SC]
stairRanges = [range(sco, sco + nCoveredSteps[i]) for i, sco in enumerate(stairOffsets)]

nSteps = sum(nCoveredSteps)
stepLengths = [stairLengths[i] // nCoveredSteps[i] for i in SC for _ in range(nCoveredSteps[i])]
stepWidths = [stairWidths[i] for i in SC for _ in range(nCoveredSteps[i])]

totalArea = sum(l * w for (l, w, _, _) in rectangles) + sum(stairLengths[i] * stairWidths[i] for i in SC)
minRollLength = (totalArea // rollWidth) + (1 if totalArea % rollWidth > 0 else 0)
totalLength = sum(max(maxLengths[i], maxWidths[i]) for i in RC) + sum(stairLengths)
maxRollLength = min(maxRollLength, totalLength)

rectSizes = range(min(min(l, w) for (l, w, _, _) in rectangles), max(max(l, w) for (l, w, _, _) in rectangles) + 1)

nexts = [next(j for j in RC if i in roomRectangles[j]) for i in range(nRectangles)]

# z is the carpet roll length
z = Var(dom=range(minRollLength, maxRollLength + 1))

# x[i] is the x-coordinate of the ith room carpet
x = VarArray(size=nRoomCarpets, dom=range(maxRollLength + 1))

# y[i] is the y-coordinate of the ith room carpet
y = VarArray(size=nRoomCarpets, dom=range(rollWidth + 1))

# r[i] is the rotation of the ith room carpet
r = VarArray(size=nRoomCarpets, dom=Rotations)

# r0or180[is] is 1 if the rotation of the ith room carpet is 0 or 180 degrees
r0or180 = VarArray(size=nRoomCarpets, dom={0, 1})

# r0or90[is] is 1 if the rotation of the ith room carpet is 0 or 90 degrees
r0or90 = VarArray(size=nRoomCarpets, dom={0, 1})

# xr[j] is the x-coordinate of the jth rectangle
xr = VarArray(size=nRectangles, dom=range(maxRollLength + 1))

# yr[j] is the y-coordinate of the jth rectangle
yr = VarArray(size=nRectangles, dom=range(rollWidth + 1))

# lr[j] is the length of the jth rectangle (considering a possible rotation)
lr = VarArray(size=nRectangles, dom=rectSizes)

# wr[j] is the width of the jth rectangle (considering a possible rotation)
wr = VarArray(size=nRectangles, dom=rectSizes)

if nSteps > 0:
    # xs[k] is the x-coordinate of the kth step of the stair
    xs = VarArray(size=nSteps, dom=range(maxRollLength + 1))

    # ys[k] is the y-coordinate of the kth step of the stair
    ys = VarArray(size=nSteps, dom=range(rollWidth + 1))

    # lp[i][j] is 1 if the jth covered step by the ith stair carpet is the last step of a part (of the partition of the stair carpet)
    lp = VarArray(size=[nStairCarpets, nCoveredSteps], dom={0, 1})

    ls, ws = stepLengths, stepWidths

else:
    xs = ys = lp = ls = ws = []

X, Y, L, W = xr + xs, yr + ys, lr + ls, wr + ws

satisfy(
    # computing lengths and widths of rectangles
    [
        (
            lr[i] == rectWidths[i] + (rectLengths[i] - rectWidths[i]) * r0or180[nexts[i]],
            wr[i] == rectLengths[i] + (rectWidths[i] - rectLengths[i]) * r0or180[nexts[i]]
        ) for i in range(nRectangles)
    ],

    # enforcing room carpets to stay within limits
    [
        (
            x[i] + maxWidths[i] + (maxLengths[i] - maxWidths[i]) * r0or180[i] <= z,
            y[i] + maxLengths[i] + (maxWidths[i] - maxLengths[i]) * r0or180[i] <= rollWidth
        ) for i in RC
    ],

    # enforcing rectangles (of room carpets) to stay within limits
    [
        (
            xr[j] + lr[j] <= z,
            yr[j] + wr[j] <= rollWidth
        ) for i in RC for j in roomRectangles[i]
    ],

    # handling possible rotations of room carpets
    [
        (
            r[i] in possibleRotations[i],
            r0or90[i] == (r[i] in {R0, R90}),
            r0or180[i] == (r[i] in {R0, R180})
        ) for i in RC
    ],

    # computing the coordinates of the rectangles in room carpets
    [
        (
            xr[j] == x[i] + xOffsets[j][r[i]],
            yr[j] == y[i] + yOffsets[j][r[i]]
        ) for i in RC for j in roomRectangles[i]
    ],

    # enforcing stair steps to stay within limits
    [
        (
            xs[j] + stepLengths[j] <= z,
            ys[j] + stepWidths[j] <= rollWidth
        ) for i in SC for j in stairRanges[i]
    ],

    # breaking symmetries between steps of a stair carpet  tag(symmetry-breaking)
    [
        (
            ys[j] <= ys[j + 1],
            If(ys[j] >= ys[j + 1], Then=xs[j] + stepLengths[j] <= xs[j + 1])
        ) for i in SC for j in stairRanges[i] if j + 1 in stairRanges[i]
    ],

    # computing the last steps in the parts of the partitions of the stair carpets
    [
        [lp[i][nCoveredSteps[i] - 1] == 1 for i in SC],

        [lp[i][j] == (ys[k] < ys[k + 1]) | (xs[k] + stepLengths[j] < xs[k + 1])
         for i, offset in enumerate(stairOffsets) for j in range(nCoveredSteps[i] - 1) if [k := j + offset]],

        [
            If(
                xs[k] + 2 * stepLengths[k] > z,
                Then=lp[i][j]
            ) for i, offset in enumerate(stairOffsets) for j in range(nCoveredSteps[i]) if [k := j + offset]
        ],

        [Sum(lp[i][:nCoveredSteps[i]]) <= maxCuts[i] + 1 for i in SC],

        [lp[i][j] == 0 for i in SC if minCutSteps[i] > 1 for j in range(minCutSteps[i] - 1)],

        [
            If(
                lp[i][j],
                Then=lp[i][k] == 0
            ) for i in SC if minCutSteps[i] > 1 for j in range(minCutSteps[i] - 1, nCoveredSteps[i]) for k in range(j - minCutSteps[i] + 1, j)
        ]
    ],

    # respecting roll length
    Cumulative(origins=X, lengths=L, heights=W) <= rollWidth,

    # respecting roll width
    Cumulative(origins=Y, lengths=W, heights=L) <= z,

    # non-overlapping
    NoOverlap(origins=zip(X, Y), lengths=zip(L, W))
)

minimize(
    # minimizing the carpet roll length
    z
)

"""
1) don't use if (k := j + offset) instead of  if (k:=j+ offset)]
  because 0 is interpreted as False, as (0) is 0 and, bool(0) is False
2) Note that:
  lp = VarArray(size=[nStairCarpets, max(nCoveredSteps)], dom=lambda i, j: {0, 1} if j < nCoveredSteps[i] else None)
 is equivalent to:
  lp = VarArray(size=[nStairCarpets, nCoveredSteps], dom={0, 1})
 because an equivalent lambda will be automatically built
"""
