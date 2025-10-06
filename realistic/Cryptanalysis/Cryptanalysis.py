"""
Chosen Key Differential Cryptanalysis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 Minizinc challenge.
The original MZN model was proposed by David Gerault, Marine Minier, and Christine Solnon - no licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integers: n, z and k

## Model
  constraints: Sum

## Execution
  python Cryptanalysis.py -data=[number,number,number]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-44953-1_37
  - https://www.minizinc.org/challenge/2016/results/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  realistic, mzn16, xcsp25
"""

from pycsp3 import *

n, z, KEY_BITS = data or (3, 4, 128)

BLOCK_BITS = 128  # Number of bits in the blocks
KC = KEY_BITS // 32  # Number of columns per round of key schedule
BC = BLOCK_BITS // 32  # Number of columns per round
NBK = KC + n * BC // KC  # Number of variables to represent the components of the key (cf. paper)

# dX[r][j][i] is 0 if the differential byte for X at round r, column j and row i is equal to 0^8
dX = VarArray(size=[n, BC, 4], dom={0, 1})  # state after ARK

# dY[r][j][i] is 0 if the differential byte for Y at round r, column j and row i is equal to 0^8
dY = VarArray(size=[n - 1, BC, 4], dom={0, 1})  # state before ARK

# dK[r][j][i] is 0 if the differential byte for K at round r, column j and row i is equal to 0^8
dK = VarArray(size=[n, BC, 4], dom={0, 1})

dSR = VarArray(size=[n, BC, 4], dom={0, 1})  # State after ShiftRows

# Kcomp[r][j][i][k] is the kth component of the key for round r, column j and row i
Kcomp = VarArray(size=[n, BC, 4, NBK], dom={0, 1})

# cX[r][j] is the sum of dX[r][][j]
cX = VarArray(size=[n, BC], dom=range(5))

# cK[r][j] is the sum of dK[r][][j]
cK = VarArray(size=[n, BC], dom=range(5))

# cSR[r][j] is the sum of dSR[r][][j]
cSR = VarArray(size=[n, BC], dom=range(5))

# eqK[r1][j1][r2][j2][i] is 1 if the byte values of dK[r1][j1][i] and dK[r2][j2][i] are equal
eqK = VarArray(size=[n, BC, n, BC, 4], dom={0, 1})

# eqY[J1][j2] is a lower bound on the equalities between MC(SB(A)) and MC(SB(B))
eqY = VarArray(size=[n * BC, n * BC], dom=lambda i, j: range(5) if i < j else None)

# eqSR[J1][j2] is a lower bound on the equalities between SR(SB(A)) and SR(SB(B))
eqSR = VarArray(size=[n * BC, n * BC], dom=lambda i, j: range(5) if i < j else None)

dff = VarArray(size=[n * BC, n * BC], dom=lambda i, j: {0, 1} if i < j else None)

XOR = lambda a, b, c: a + b + c != 1  # regular xor, except 1 xor 1 can be either 0 or 1
XOR2 = lambda a, b, c, eqab, eqac, eqbc: [a + b + c != 1, eqab == 1 - c, eqac == 1 - b, eqbc == 1 - a]  # xor with equivalence propagation

idxa1 = [(J, J // BC, J % BC, (J - KC) // BC, (J - KC) % BC, (J - 1) // BC, (J + BC - 1) % BC) for J in range(BC * n)]
idxa2 = [v for v in idxa1 if v[0] >= KC]


def init_KS(J, r1, j1, r2, j2, r3, j3, i, k):
    if J < KC:  # for the first key schedule round
        return Kcomp[r1][j1][i][k] == (dK[r1][j1][i] if k == J else 0)
    if J % KC == 0:  # else, for SB positions (for AES 128, corresponds to the first column of dK for each round)
        return Kcomp[r1][j1][i][k] == (dK[r3][j3][i + 1] if k == (J // KC) * BC + j1 else Kcomp[r2][j2][i][k])
    return None


def aux_KS(J, r1, j1, r2, j2, r3, j3, i):
    if J % KC == 0:
        return XOR(dK[r2][j2][i], dK[r3][j3][(i + 1) % 4], dK[r1][j1][i])
    return [
        XOR2(dK[r2][j2][i], dK[r3][j3][i], dK[r1][j1][i], eqK[r3][j3][r2][j2][i], eqK[r1][j1][r2][j2][i], eqK[r1][j1][r3][j3][i]),
        [Kcomp[r1][j1][i][k] == (Kcomp[r2][j2][i][k] * dK[r2][j2][i] != Kcomp[r3][j3][i][k] * dK[r3][j3][i]) for k in range(NBK)]
    ]


satisfy(
    # ensuring the goal is reached
    Sum(cSR) + Sum(cK[J // BC][J % BC] for J in range(BC * n) if J % KC == KC - 1) == z,

    # initialisation of the redundant variables
    [
        (
            cX[r][j] == Sum(dX[r][j]),
            cK[r][j] == Sum(dK[r][j]),
            cSR[r][j] == Sum(dSR[r][j])
        ) for r in range(n) for j in range(BC)
    ],

    # ARK (Add Round Key)
    [XOR(dY[r - 1][j][i], dK[r][j][i], dX[r][j][i]) for r in range(1, n) for j in range(BC) for i in range(4)],

    # ensuring Maximum Distance Separable (MDS) property of Mix Columns (MC)
    [
        [dSR[r][j][i] == dX[r][j + i][i] for r in range(n) for j in range(BC) for i in range(4)],
        [cSR[r][j] + Sum(dY[r][j]) in {0, 5, 6, 7, 8} for r in range(n - 1) for j in range(BC)]
    ],

    # KS (key Schedule)
    [
        [init_KS(*v, i, k) for v in idxa1 for i in range(4) for k in range(NBK)],
        [aux_KS(*v, i) for v in idxa2 for i in range(4)],
        [Sum(Kcomp[J // BC][J % BC][i]) + dK[J // BC][J % BC][i] != 1 for J in range(KC, n * BC) for i in range(4)]
    ],

    # equality relations: if (in byte values) dK[r1][j1][i] == dK[r2][j2][i] and dK[r2][j2][i] == dK[r3][j3][i] then dK[r1][j1][i] == dK[r3][j3][i]
    [
        (
            If(  # EQ(a,b) => A=B
                eqK[r1][j1][r2][j2][i],
                Then=dK[r1][j1][i] == dK[r2][j2][i]
            ),

            eqK[r1][j1][r2][j2][i] == eqK[r2][j2][r1][j1][i],  # symmetry

            If(  # Va=Vb => EQ(a,b)
                [Kcomp[r1][j1][i][k] == Kcomp[r2][j2][i][k] for k in range(NBK)],
                Then=eqK[r1][j1][r2][j2][i] == 1
            ),

            Sum(dK[r1][j1][i], dK[r2][j2][i], eqK[r1][j1][r2][j2][i]) != 0,  # a+b+EQ(a,b) !=0

            [Sum(eqK[r1][j1][r3][j3][i], eqK[r1][j1][r2][j2][i], eqK[r2][j2][r3][j3][i]) != 2 for r3 in range(n) for j3 in range(BC)]  # transitivity

        ) for J1, J2 in combinations(n * BC, 2) if (r1 := J1 // BC, j1 := J1 % BC, r2 := J2 // BC, j2 := J2 % BC) for i in range(4)
    ],

    # linear Mix Columns
    [
        (
            dff[J1][J2] == Exist(
                disjunction(
                    dSR[r1 - 1][j1][i] != dSR[r2 - 1][j2][i],  # different bit values
                    dY[r1 - 1][j1][i] != dY[r2 - 1][j2][i],  # different after MC (since A==b => MC(A) == MC(B))
                    eqK[r1][j1][r2][j2][i] + dX[r1][j1][i] + dX[r2][j2][i] == 0,  # MC(SB(A)) xor K1 + MC(SB(B)) xor K2 = 0 and not(EQ(K1, K2))
                    (eqK[r1][j1][r2][j2][i] + dK[r1][j1][i] == 2) & (dX[r1][j1][i] != dX[r2][j2][i])  # MC(SB(A)) xor K != MC(SB(B)) xor K
                ) for i in range(4)
            ),

            eqSR[J1][J2] == Sum(  # lower bound on the equalities between SR(SB(A)) and SR(SB(B))
                dSR[r1 - 1][j1][i] + dSR[r2 - 1][j2][i] == 0 for i in range(4)
            ),

            eqY[J1][J2] == Sum(  # lower bound on the equalities between MC(SB(A)) and MC(SB(B))
                either(
                    both(eqK[r1][j1][r2][j2][i], dX[r1][j1][i] + dX[r2][j2][i] == 0),
                    dY[r1 - 1][j1][i] + dY[r2 - 1][j2][i] == 0
                ) for i in range(4)
            )
        ) for J1, J2 in combinations(range(BC, n * BC), 2) if (r1 := J1 // BC, j1 := J1 % BC, r2 := J2 // BC, j2 := J2 % BC)
    ],

    [  # If S(A) != S(B) (in bytes) then MDS Property
        If(
            dff[J1][J2],
            Then=eqSR[J1][J2] + eqY[J1][J2] <= 3
        ) for J1, J2 in combinations(range(BC, n * BC), 2)
    ]
)

""" Comments
1) Data used in 2016 are : (5,11,128) (5,14,128) (5,16,128) (5,17,128) (7,10,192)
2) Auto-adjustment of array indexing is used:
 For example, deX[r][j + i][i] is equivalent to dX[r][(j + i) % BC][i]
3) data used for the 2025 XCSP3 Competition are: [(3, 4, 128), (3, 5, 128), (4, 9, 128), (4, 11, 128), (4, 12, 128), (5, 10, 128), (5, 14, 128), (5, 15, 128), 
  (6, 12, 128), (6, 16, 128), (6, 17, 128)]
"""

# maximize(
#      Sum(cSR) + Sum(cK[J // BC, J % BC] for J in range(BC * n) if J % KC == KC - 1)
# )
