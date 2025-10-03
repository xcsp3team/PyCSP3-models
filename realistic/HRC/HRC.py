"""
The Hospitals/Residents problem with Couples (HRC) models the allocation of intending junior doctors to hospitals
where couples are allowed to submit joint preference lists over pairs of (typically geographically close) hospitals.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2019 Minizinc challenges.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  exp1-1-5460.json

## Model
  constraints: Count, Sum

## Execution
  python HRC.py -data=<datafile.json>
  python HRC.py -data=<datafile.dzn> -parser=HRC_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-016-9249-7
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn17, mzn19
"""

from pycsp3 import *

nBlockingPairs, nCouples, r_preferences, hospitals = data or load_json_data("exp1-1-5460.json")

OFFSET = 2 * nCouples  # offset for getting single lists : r_preferences sis composed of 2*nCouples entries followed by nSingles entries

h_preferences, h_ranks, h_capacities = zip(*hospitals)
nResidents, nHospitals = len(r_preferences), len(h_preferences)
nSingles = nResidents - OFFSET

maxResPref = max(len(row) - 1 for row in r_preferences)  # -1 because there is an artificial value at the end of each resident list
maxHosPref = max(len(row) for row in h_preferences)


def hosp_would_prefer(h, q, gap=0):  # NB! q < h_capacities[h] - gap or q <= h_capacities[h] - gap as it seems to be in the MZN model
    return disjunction(
        q < h_capacities[h] - gap,
        Sum(ha[h, :q]) < h_capacities[h] - gap,
        Sum(ha[h, q + 1:len(h_preferences[h])]) > gap
    )


def hosp_would_prefer_exc(h1, h2, q1, q2):
    if h2 == h1 and q2 > q1:
        return Sum(ha[h1, :q1]) + ha[h1, q2] < h_capacities[h1]
    return Sum(ha[h1, :q1]) < h_capacities[h1]


def type1(i, j):
    h = r_preferences[OFFSET + i][j]
    q = h_ranks[h][OFFSET + i]
    return hosp_would_prefer(h, q)


def type2(i, j):
    r1, r2 = i * 2, i * 2 + 1
    h1, h2 = r_preferences[r1][j], r_preferences[r2][j]
    q1, q2 = h_ranks[h1][r1], h_ranks[h2][r2]
    return either(
        both(
            h2 == r_preferences[r2][cp[i]],
            hosp_would_prefer_exc(h1, h2, q1, q2)
        ),
        both(
            h1 == r_preferences[r1][cp[i]],
            hosp_would_prefer_exc(h2, h1, q2, q1)
        )
    )


def type3(i, j):
    r1, r2 = i * 2, i * 2 + 1
    assert r_preferences[r1][j] != r_preferences[r2][j]
    h1, h2 = r_preferences[r1][j], r_preferences[r2][j]
    q1, q2 = h_ranks[h1][r1], h_ranks[h2][r2]
    return conjunction(
        h2 != r_preferences[r2][cp[i]],
        h1 != r_preferences[r1][cp[i]],
        hosp_would_prefer(h1, q1),
        hosp_would_prefer(h2, q2)
    )


def type4(i, j):
    r1, r2 = i * 2, i * 2 + 1
    assert r_preferences[r1][j] == r_preferences[r2][j]
    h = r_preferences[r1][j]
    q1, q2 = h_ranks[h][r1], h_ranks[h][r2]
    q_min, q_max = (q1, q2) if q1 < q2 else (q2, q1)
    return conjunction(
        h != r_preferences[r2][cp[i]],
        h != r_preferences[r1][cp[i]],
        both(hosp_would_prefer(h, q_min, 1), hosp_would_prefer(h, q_max))
    )


C, S, H = range(nCouples), range(nSingles), range(nHospitals)

CMAX = [len(r_preferences[2 * i]) - 1 for i in C]  # -1 because of the special value at the end of these lists
SMAX = [len(r_preferences[OFFSET + i]) - 1 for i in S]  # -1 because of the special value at the end of these lists
HMAX = [len(h_preferences[i]) for i in H]

CR, SR = [range(CMAX[i]) for i in C], [range(SMAX[i]) for i in S]

# cbp[i][j] is 1 if the jth preference of the ith couple is blocked
cbp = VarArray(size=[nCouples, maxResPref], dom=lambda i, j: {0, 1} if j < CMAX[i] else None)

# sbp[i][j] is 1 if the jth preference of the ith single is blocked
sbp = VarArray(size=[nSingles, maxResPref], dom=lambda i, j: {0, 1} if j < SMAX[i] else None)

# ca[i][j] is 1 if the ith couple is assigned its jth preferred hospital
ca = VarArray(size=[nCouples, maxResPref], dom={0, 1})

# sa[i][j] is 1 if the ith single is assigned its jth preferred hospital
sa = VarArray(size=[nSingles, maxResPref], dom={0, 1})

# c_unassigned[i] is 1 if the ith couple is unassigned
c_unassigned = VarArray(size=nCouples, dom={0, 1})

# s_unassigned[i] is 1 if the ith single is unassigned
s_unassigned = VarArray(size=nSingles, dom={0, 1})

# cp[i] is the position the ith couple gets in its preference list (or -1)
cp = VarArray(size=nCouples, dom=lambda i: range(CMAX[i] + 1))

# sp[i] is the position the ith single gets in its preference list (or -1)
sp = VarArray(size=nSingles, dom=lambda i: range(SMAX[i] + 1))

# ha[i][j] is 1 if the ith hospital i is assigned its jth preferred resident
ha = VarArray(size=[nHospitals, maxHosPref], dom=lambda i, j: {0, 1} if j < HMAX[i] else {0})

satisfy(
    # ensuring that we have exactly the target number of blocking pairs
    Sum(cbp) + Sum(sbp) == nBlockingPairs,

    # computing (and linking) assignments of singles
    [
        [s_unassigned[i] == (sp[i] == SMAX[i]) for i in S],
        [sa[i][j] == (sp[i] == j) for i in S for j in SR[i]]
    ],

    # computing (and linking) assignments of couples
    [
        [c_unassigned[i] == (cp[i] == CMAX[i]) for i in C],
        [ca[i][j] == (cp[i] == j) for i in C for j in CR[i]]
    ],

    # matching assignments of singles and hospitals
    [sa[i][j] == ha[p][k] for i in S for j, p in enumerate(r_preferences[OFFSET + i]) if p != -1 and (k := h_ranks[p][OFFSET + i]) >= 0],

    # matching assignments of couples and hospitals
    [ha[i][j] == ExactlyOne(ca[p // 2][k] for k in CR[p // 2] if r_preferences[p][k] == i) for i in H for j, p in enumerate(h_preferences[i]) if p < OFFSET],

    # respecting hospital capacities
    [Sum(ha[i]) <= h_capacities[i] for i in H],

    # computing blocking pairs
    [
        [
            If(
                sp[i] > j, type1(i, j),
                Then=sbp[i][j]
            ) for i in S for j in SR[i]
        ],
        [
            If(
                cp[i] > j, type2(i, j),
                Then=cbp[i][j]
            ) for i in C for j in CR[i]
        ],
        [
            If(
                cp[i] > j, type3(i, j),
                Then=cbp[i][j]
            ) for i in C for j in CR[i] if r_preferences[2 * i][j] != r_preferences[2 * i + 1][j]
        ],
        [
            If(
                cp[i] > j, type4(i, j),
                Then=cbp[i][j]
            ) for i in C for j in CR[i] if r_preferences[2 * i][j] == r_preferences[2 * i + 1][j]
        ]
    ]
)

minimize(
    # minimizing the number of residents being unassigned
    2 * Sum(c_unassigned) + Sum(s_unassigned)
)

""" Comments
1) Since oct 2025, we can write: If(sp[i] > j, type1(i, j), Then= 
   we are no more obliged to keep using & and |
   as for example in If(sp[i] > j) & type1(i, j), Then=
"""

# coup_pos == decrement([1, 2, 4, 2, 1, 8, 5, 3, 3, 11, 3, 1, 13, 6, 1, 2, 2, 14, 6, 3, 3, 1, 10, 7, 3]),
# single_pos ==  decrement([1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 4, 2, 2, 2, 2, 5, 3, 1, 2, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 4, 1, 1, 4,1]),


# def hosp_would_prefer(h, q, gap=0):  # NB! q < h_capacities[h] - gap or q <= h_capacities[h] - gap as it seems to be in the MZN model
# if q < h_capacities[h] - gap:
#     return True
# return either(
#     Sum(ha[h, :q]) < h_capacities[h] - gap,
#     Sum(ha[h, q + 1:len(h_preferences[h])]) > gap
# )
