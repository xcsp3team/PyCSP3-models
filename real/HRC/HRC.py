"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  exp1-1-5460.json

## Model
  constraints: Count, Sum

## Execution
  python HRC.py -data=<datafile.json>
  python HRC.py -data=<datafile.dzn> -parser=HRC_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  real, mzn17, mzn19
"""

from pycsp3 import *

nBlockingPairs, nCouples, rpref, rpref_len, hospitals = data
assert all(len(rpref[i]) - 1 == rpref_len[i] for i in range(len(rpref)))
h_preferences, h_ranks, h_capacities = zip(*hospitals)
nResidents, nHospitals = len(rpref), len(h_preferences)
OFFSET = 2 * nCouples  # offset for singles
Singles = range(OFFSET, nResidents)
nSingles = nResidents - OFFSET
assert nSingles == len(Singles)

max_rpref = max(len([v for v in row if v != -1]) for row in rpref)
max_hpref = max(len(row) for row in h_preferences)


def hosp_would_prefer(h, q, gap=0):  # NB! q < h_capacities[h] - gap or q <= h_capacities[h] - gap as it seems to be in the MZN model
    if q < h_capacities[h] - gap:
        return True
    return (Sum(ha[h, :q]) < h_capacities[h] - gap) | (Sum(ha[h, q + 1:len(h_preferences[h])]) > gap)


def hosp_would_prefer_exc(h1, h2, q1, q2):
    if h2 == h1 and q2 > q1:
        return Sum(ha[h1, :q1]) + ha[h1, q2] < h_capacities[h1]
    return Sum(ha[h1, :q1]) < h_capacities[h1]


def type1(i, j):
    h = rpref[2 * nCouples + i][j]
    q = h_ranks[h][2 * nCouples + i]
    return hosp_would_prefer(h, q)


def type2(i, j):
    r1, r2 = i * 2, i * 2 + 1
    h1, h2 = rpref[r1][j], rpref[r2][j]
    q1, q2 = h_ranks[h1][r1], h_ranks[h2][r2]
    return ((h2 == rpref[r2][cp[i]]) & hosp_would_prefer_exc(h1, h2, q1, q2)) | ((h1 == rpref[r1][cp[i]]) & hosp_would_prefer_exc(h2, h1, q2, q1))


def type3(i, j):
    r1, r2 = i * 2, i * 2 + 1
    assert rpref[r1][j] != rpref[r2][j]
    h1, h2 = rpref[r1][j], rpref[r2][j]
    q1, q2 = h_ranks[h1][r1], h_ranks[h2][r2]
    return (h2 != rpref[r2][cp[i]]) & (h1 != rpref[r1][cp[i]]) & hosp_would_prefer(h1, q1) & hosp_would_prefer(h2, q2)


def type4(i, j):
    r1, r2 = i * 2, i * 2 + 1
    assert rpref[r1][j] == rpref[r2][j]
    h = rpref[r1][j]
    q1, q2 = h_ranks[h][r1], h_ranks[h][r2]
    sub = hosp_would_prefer(h, q1, 1) & hosp_would_prefer(h, q2) if q1 < q2 else hosp_would_prefer(h, q2, 1) & hosp_would_prefer(h, q1)
    return (h != rpref[r2][cp[i]]) & (h != rpref[r1][cp[i]]) & sub


# cbp[i][j] is 1 if the jth preference of the ith couple is blocked
cbp = VarArray(size=[nCouples, max_rpref], dom=lambda i, j: {0, 1} if j < rpref_len[2 * i] else None)

# sbp[i][j] is 1 if the jth preference of the ith single is blocked
sbp = VarArray(size=[nSingles, max_rpref], dom=lambda i, j: {0, 1} if j < rpref_len[OFFSET + i] else None)

# ca[i][j] is 1 if the ith couple is assigned its jth preferred hospital
ca = VarArray(size=[nCouples, max_rpref], dom={0, 1})

# sa[i][j] is 1 if the ith single is assigned its jth preferred hospital
sa = VarArray(size=[nSingles, max_rpref], dom={0, 1})

# c_unassigned[i] is 1 if the ith couple is unassigned
c_unassigned = VarArray(size=nCouples, dom={0, 1})

# s_unassigned[i] is 1 if the ith single is unassigned
s_unassigned = VarArray(size=nSingles, dom={0, 1})

# cp[i] is the position the ith couple gets in its preference list (or -1)
cp = VarArray(size=nCouples, dom=lambda i: range(rpref_len[2 * i] + 1))

# sp[i] is the position the ith single gets in its preference list (or -1)
sp = VarArray(size=nSingles, dom=lambda i: range(rpref_len[OFFSET + i] + 1))

# ha[i][j] is 1 if the ith hospital i is assigned its jth preferred resident
ha = VarArray(size=[nHospitals, max_hpref], dom=lambda i, j: {0, 1} if 0 <= j < len(h_preferences[i]) else {0})

satisfy(
    # ensuring that we have exactly the target number of blocking pairs
    Sum(cbp) + Sum(sbp) == nBlockingPairs,

    # computing (and linking) assignments of singles
    [
        [s_unassigned[i] == (sp[i] == rpref_len[OFFSET + i]) for i in range(nSingles)],
        [sa[i][j] == (sp[i] == j) for i in range(nSingles) for j in range(rpref_len[OFFSET + i])]
    ],

    # computing (and linking) assignments of couples
    [
        [c_unassigned[i] == (cp[i] == rpref_len[2 * i]) for i in range(nCouples)],
        [ca[i][j] == (cp[i] == j) for i in range(nCouples) for j in range(rpref_len[2 * i])]
    ],

    # matching assignments of singles and hospitals
    [sa[i][j] == ha[p][h_ranks[p][OFFSET + i]]
     for i in range(nSingles) for j, p in enumerate(rpref[OFFSET + i]) if p != -1 and h_ranks[p][OFFSET + i] >= 0],

    # matching assignments of couples and hospitals
    [ha[i][j] == ExactlyOne(ca[p // 2][k] for k in range(rpref_len[p]) if rpref[p][k] == i)
     for i in range(nHospitals) for j, p in enumerate(h_preferences[i]) if p < OFFSET],

    # respecting hospital capacities
    [Sum(ha[i]) <= h_capacities[i] for i in range(nHospitals)],

    # computing blocking pairs
    [
        [
            If(
                (sp[i] > j) & type1(i, j),
                Then=sbp[i][j]
            ) for i in range(nSingles) for j in range(rpref_len[OFFSET + i])
        ],
        [
            If(
                (cp[i] > j) & type2(i, j),
                Then=cbp[i][j]
            ) for i in range(nCouples) for j in range(rpref_len[2 * i])
        ],
        [
            If(
                (cp[i] > j) & type3(i, j),
                Then=cbp[i][j]
            ) for i in range(nCouples) for j in range(rpref_len[2 * i]) if rpref[2 * i][j] != rpref[2 * i + 1][j]
        ],
        [
            If(
                (cp[i] > j) & type4(i, j),
                Then=cbp[i][j]
            ) for i in range(nCouples) for j in range(rpref_len[2 * i]) if rpref[2 * i][j] == rpref[2 * i + 1][j]
        ]
    ]
)

minimize(
    # minimizing the number of residents being unassigned
    2 * Sum(c_unassigned) + Sum(s_unassigned)
)

"""
1) because the way constraint terms and Boolean terms are mixed, we need to keep using & and |
   as for example in If(sp[i] > j) & type1(i, j), Then=
   with this current form, we cannot write: If(sp[i] > j, type1(i, j), Then= 
"""

# coup_pos == decrement([1, 2, 4, 2, 1, 8, 5, 3, 3, 11, 3, 1, 13, 6, 1, 2, 2, 14, 6, 3, 3, 1, 10, 7, 3]),
# single_pos ==  decrement([1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 4, 2, 2, 2, 2, 5, 3, 1, 2, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 4, 1, 1, 4,1]),
