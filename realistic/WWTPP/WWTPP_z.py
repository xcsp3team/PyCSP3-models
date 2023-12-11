"""
Waste Water Treatment Plant Scheduling Problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011 Minizinc challenges.
The MZN model was proposed by Miquel Bofill.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  02840.json

## Model
  constraints: Sum

## Execution
  python WWTPP_z.py -data=<datafile.json>
  python WWTPP_z.py -data=<datafile.dzn> -parser=WWTPP_ParserZ.py

## Links
  - https://arxiv.org/abs/1609.05367
  - https://www.minizinc.org/challenge2011/results2011.html

## Tags
  realistic, mzn10, mzn11
"""

from pycsp3 import *

plant_capacity, flows, capacities, d = data
nIndustries, nSteps = 8, 24  # len(d), len(d[0])

T1 = ([(1, 1)] + [(1, i) for i in range(2, 25, 2)] + [(2, i) for i in range(1, 13)] + [(2, i) for i in range(14, 25)]
      + [(3, i) for i in (1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 17, 18, 19, 20, 22, 23, 24)]
      + [(5, i) for i in list(range(1, 6)) + list(range(7, 16)) + list(range(17, 25))]
      + [(6, i) for i in (1, 4, 5, 6, 7, 11, 12, 14, 15, 17, 18, 19, 20, 23, 24)] + [(7, 24)]
      + [(8, i) for i in (1, 2, 4, 6, 8, 10, 12, 13, 14)])

T2 = ([(1, i) for i in range(3, 24, 2)] + [(2, 13)] + [(3, 10), (3, 21)] + [(4, i) for i in range(1, 25)] + [(5, 6), (5, 16)]
      + [(6, 13), (6, 16)] + [(7, i) for i in range(1, 24)] + [(8, i) for i in [3, 5, 7, 9, 11] + list(range(15, 25))])

# sf[i][j] is the flow stored in buffer i at the end of time period j
sf = VarArray(size=[nIndustries, nSteps], dom=range(max(capacities) + 1))

# df[i][j] is the flow discharged from buffer (of industry) i during time period j
df = VarArray(size=[nIndustries, nSteps], dom=range(max(flows) + 1))

# c[i][j] is the actual capacity requirement of industry i during time period j
c = VarArray(size=[nIndustries, nSteps], dom=range(max(max(row) for row in d) + 1))

satisfy(
    # ensuring that the capacity of the plant is not exceeded at any time
    [Sum(c[i][j] + df[i][j] for i in range(nIndustries)) <= plant_capacity for j in range(nSteps)],

    # computing the amount of water inside every buffer at any time
    [
        (
            sf[i][0] == d[i][0] - c[i][0],
            [sf[i][j] == sf[i][j - 1] - df[i][j] + d[i][j] - c[i][j] for j in range(1, nSteps)],
            sf[i][-1] == 0
        ) for i in range(nIndustries)
    ],

    # ensuring that the capacity of each buffer is not exceeded at any time
    [sf[i][j] <= capacities[i] for i in range(nIndustries) for j in range(nSteps)],

    # imposing restrictions on the output flow from the buffers
    [
        [df[i][0] == 0 for i in range(nIndustries)],
        [
            If(
                df[i][j] != 0,
                Then=If(
                    sf[i][j - 1] > flows[i],
                    Then=df[i][j] == flows[i],
                    Else=df[i][j] == sf[i][j - 1]
                )
            ) for i in range(nIndustries) for j in range(1, nSteps)
        ]
    ],

    # tag(redundant-constraints)
    [
        [df[i][j] <= flows[i] for i in range(nIndustries) for j in range(nSteps)],
        [df[i][j] <= sf[i][j - 1] for i in range(nIndustries) for j in range(1, nSteps)]
    ],

    [c[i - 1][j - 1] == 0 for i, j in T1],
    [
        If(
            c[i - 1][j - 1] != 0,
            Then=c[i - 1][j - 1] == d[i - 1][j - 1]
        ) for i, j in T2
    ],

    # restrictions on discharges wrt time periods
    [
        ((c[2][3] == 0) & (c[2][4] == 0)) | ((c[2][3] == d[2][3]) & (c[2][4] == d[2][4])),
        ((c[2][13] == 0) & (c[2][14] == 0) & (c[2][15] == 0)) | ((c[2][13] == d[2][13]) & (c[2][14] == d[2][14]) & (c[2][15] == d[2][15])),
        ((c[5][1] == 0) & (c[5][2] == 0)) | ((c[5][1] == d[5][1]) & (c[5][2] == d[5][2])),
        ((c[5][7] == 0) & (c[5][8] == 0) & (c[5][9] == 0)) | ((c[5][7] == d[5][7]) & (c[5][8] == d[5][8]) & (c[5][9] == d[5][9])),
        ((c[5][20] == 0) & (c[5][21] == 0)) | ((c[5][20] == d[5][20]) & (c[5][21] == d[5][21]))
    ]
)

"""
1) The If statement above is equivalent to:
 [(df[i][j] == 0) | ((df[i][j] == flows[i]) & (sf[i][j - 1] > flows[i])) | ((df[i][j] == sf[i][j - 1]) & (sf[i][j - 1] <= flows[i]))
"""
