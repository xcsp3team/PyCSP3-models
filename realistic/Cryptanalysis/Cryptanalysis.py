"""
Chosen Key Differential Cryptanalysis.

Differential cryptanalysis aims at evaluating confidentiality by testing whether it is possible to find the secret key within a reasonable number of trials.
One can use Constraint Programming models to solve the chosen key differential attack against the standard block cipher AES (se paper cited below).
In the first step, there is a search for binary solutions.
Each unknown delta X_i  is modeled with a 4 x 4 byte matrix, and a binary variable is associated with every differential byte of the unknown.
These binary variables are equal to 0 if their associated differential bytes are equal to 0^8, and they are equal to 1 otherwise.
We also associate binary variables with every differential byte in delta K_i and delta Y_i, respectively.
The operations that transform delta X into delta X_r (obtained after applying the round function r times) are translated into constraints between these binary variables.
For the first step, the goal is then to find solutions which satisfy these constraints (and solutions are called binary solutions).

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

nRounds, z, nBits = data or (3, 4, 128)  # z (objective value) and number of bits in the key

m, n = 4, 4  # number of columns (BC) and rows per round
KC = nBits // 32  # number of columns per round of key schedule
NBK = KC + nRounds * m // KC  # number of variables to represent the components of the key (cf. paper)

R, J, I, Q = range(nRounds), range(m), range(n), range(nRounds * m)  # rounds, columns, rows

V = [(q, q // m, q % m, (q - KC) // m, (q - KC) % m, (q - 1) // m, (q - 1 + m) % m) for q in Q]

# dX[r][j][i] is 0 if the differential byte for X at round r, column j and row i is equal to 0^8
dX = VarArray(size=[R, J, I], dom={0, 1})  # state after ARK (AddRoundKey)

# dY[r][j][i] is 0 if the differential byte for Y at round r, column j and row i is equal to 0^8
dY = VarArray(size=[R[:-1], J, I], dom={0, 1})  # state before ARK

# dK[r][j][i] is 0 if the differential byte for K at round r, column j and row i is equal to 0^8
dK = VarArray(size=[R, J, I], dom={0, 1})

# dSR[r][j][i] is the state after SR at round r, column j and row i
dSR = VarArray(size=[R, J, I], dom={0, 1})  # state after SR (ShiftRows)

# key[r][j][i][k] is the kth component of the key for round r, column j and row i
key = VarArray(size=[R, J, I, NBK], dom={0, 1})

# cX[r][j] is the sum of dX[r][][j]
cX = VarArray(size=[R, J], dom=range(m + 1))

# cK[r][j] is the sum of dK[r][][j]
cK = VarArray(size=[R, J], dom=range(m + 1))

# cSR[r][j] is the sum of dSR[r][][j]
cSR = VarArray(size=[R, J], dom=range(m + 1))

# eqK[r1][j1][r2][j2][i] is 1 if the byte values of dK[r1][j1][i] and dK[r2][j2][i] are equal
eqK = VarArray(size=[R, J, R, J, I], dom={0, 1})

# eqY[q1][q2] is a lower bound on the equalities between MC(SB(A)) and MC(SB(B))
eqY = VarArray(size=[Q, Q], dom=lambda q1, q2: range(n + 1) if q1 < q2 else None)

# eqSR[q1][q2] is a lower bound on the equalities between SR(SB(A)) and SR(SB(B))
eqSR = VarArray(size=[Q, Q], dom=lambda q1, q2: range(n + 1) if q1 < q2 else None)

dff = VarArray(size=[Q, Q], dom=lambda q1, q2: {0, 1} if q1 < q2 else None)


def XOR(a, b, c, eq_ab=None, eq_ac=None, eq_bc=None):
    assert (eq_ab is None) == (eq_ac is None) == (eq_bc is None)
    if eq_ab is None:
        return a + b + c != 1  # regular xor, except 1 xor 1 can be either 0 or 1
    else:
        return [a + b + c != 1, eq_ab == 1 - c, eq_ac == 1 - b, eq_bc == 1 - a]  # xor with equivalence propagation


def init_KS(q, r1, j1, r2, j2, r3, j3, i, k):
    if q < KC:  # for the first key schedule round
        if k == q:
            return key[r1][j1][i][k] == dK[r1][j1][i]
        else:
            return key[r1][j1][i][k] == 0
    if q % KC == 0:  # else, for SB positions (for AES 128, corresponds to the first column of dK for each round)
        if k == (q // KC) * m + j1:
            return key[r1][j1][i][k] == dK[r3][j3][i + 1]
        else:
            return key[r1][j1][i][k] == key[r2][j2][i][k]
    return None


def aux_KS(q, r1, j1, r2, j2, r3, j3, i):
    if q % KC == 0:
        return XOR(dK[r2][j2][i], dK[r3][j3][i + 1], dK[r1][j1][i])
    return (
        XOR(
            dK[r2][j2][i], dK[r3][j3][i], dK[r1][j1][i],
            eqK[r3][j3][r2][j2][i], eqK[r1][j1][r2][j2][i], eqK[r1][j1][r3][j3][i]
        ),
        [key[r1][j1][i][k] == (key[r2][j2][i][k] * dK[r2][j2][i] != key[r3][j3][i][k] * dK[r3][j3][i]) for k in range(NBK)]
    )


satisfy(
    # ensuring the goal is reached
    Sum(cSR) + Sum(cK[:, KC - 1]) == z,

    # initialisation of the redundant variables
    [
        (
            cX[r][j] == Sum(dX[r][j]),
            cK[r][j] == Sum(dK[r][j]),
            cSR[r][j] == Sum(dSR[r][j])
        ) for r in R for j in J
    ],

    # operation ARK (AddRoundKey)
    [XOR(dY[r - 1][j][i], dK[r][j][i], dX[r][j][i]) for r in R[1:] for j in J for i in I],

    # ensuring Maximum Distance Separable (MDS) property of Mix Columns (MC)
    [
        [dSR[r][j][i] == dX[r][j + i][i] for r in R for j in J for i in I],
        [cSR[r][j] + Sum(dY[r][j]) in {0, 5, 6, 7, 8} for r in R[:-1] for j in J]
    ],

    # operation KS (KeySchedule)
    [
        [init_KS(*v, i, k) for v in V for i in I for k in range(NBK)],
        [aux_KS(*v, i) for v in V if v[0] >= KC for i in I],
        [Sum(key[r][j][i]) + dK[r][j][i] != 1 for r in R for j in J if r * m + j >= KC for i in I]
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
                [key[r1][j1][i][k] == key[r2][j2][i][k] for k in range(NBK)],
                Then=eqK[r1][j1][r2][j2][i] == 1
            ),

            Sum(dK[r1][j1][i], dK[r2][j2][i], eqK[r1][j1][r2][j2][i]) != 0,  # a+b+EQ(a,b) !=0

            [Sum(eqK[r1][j1][r3][j3][i], eqK[r1][j1][r2][j2][i], eqK[r2][j2][r3][j3][i]) != 2 for r3 in R for j3 in J]  # transitivity
        ) for q1, q2 in combinations(Q, 2) if (r1 := q1 // m, j1 := q1 % m, r2 := q2 // m, j2 := q2 % m) for i in I
    ],

    # operation linear MC (MixColumns)
    [
        (
            dff[q1][q2] == Exist(
                disjunction(
                    dSR[r1 - 1][j1][i] != dSR[r2 - 1][j2][i],  # different bit values
                    dY[r1 - 1][j1][i] != dY[r2 - 1][j2][i],  # different after MC (since A==b => MC(A) == MC(B))
                    eqK[r1][j1][r2][j2][i] + dX[r1][j1][i] + dX[r2][j2][i] == 0,  # MC(SB(A)) xor K1 + MC(SB(B)) xor K2 = 0 and not(EQ(K1, K2))
                    both(  # MC(SB(A)) xor K != MC(SB(B)) xor K
                        eqK[r1][j1][r2][j2][i] + dK[r1][j1][i] == 2,
                        dX[r1][j1][i] != dX[r2][j2][i]
                    )
                ) for i in I
            ),

            eqSR[q1][q2] == Sum(dSR[r1 - 1][j1][i] + dSR[r2 - 1][j2][i] == 0 for i in I),  # lower bound on the equalities between SR(SB(A)) and SR(SB(B))

            eqY[q1][q2] == Sum(  # lower bound on the equalities between MC(SB(A)) and MC(SB(B))
                either(
                    both(eqK[r1][j1][r2][j2][i], dX[r1][j1][i] + dX[r2][j2][i] == 0),
                    dY[r1 - 1][j1][i] + dY[r2 - 1][j2][i] == 0
                ) for i in I
            )
        ) for q1, q2 in combinations(Q[m:], 2) if (r1 := q1 // m, j1 := q1 % m, r2 := q2 // m, j2 := q2 % m)
    ],

    [  # If S(A) != S(B) (in bytes) then MDS Property
        If(
            dff[q1][q2],
            Then=eqSR[q1][q2] + eqY[q1][q2] <= 3
        ) for q1, q2 in combinations(Q[m:], 2)
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

# BLOCK_BITS = 128  # number of bits in the blocks
# BC = BLOCK_BITS_BITS // 32  # number of columns per round
