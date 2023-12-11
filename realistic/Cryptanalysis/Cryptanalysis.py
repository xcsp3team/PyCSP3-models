"""
Chosen Key Differential Cryptanalysis.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 Minizinc challenge.
The MZN model was proposed by David Gerault, Marine Minier, and Christine Solnon.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  three integers

## Model
  constraints: Sum

## Execution
  python Cryptanalysis.py -data=<n,z,k>

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-44953-1_37
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn16
"""

from pycsp3 import *

n, z, KEY_BITS = data

BLOCK_BITS = 128  # Number of bits in the blocks
KC = KEY_BITS // 32  # Number of columns per round of key schedule
BC = BLOCK_BITS // 32  # Number of columns per round
NBK = KC + n * BC // KC  # Number of variables to represent the components of the key (cf. paper)

deltaY = VarArray(size=[n - 1, BC, 4], dom={0, 1})  # State before ARK

deltaX = VarArray(size=[n, BC, 4], dom={0, 1})  # State after ARK

deltaSR = VarArray(size=[n, BC, 4], dom={0, 1})  # State after ShiftRows

deltaK = VarArray(size=[n, BC, 4], dom={0, 1})  # Key

Kcomp = VarArray(size=[n, BC, 4, NBK], dom={0, 1})  # The components of the key

eqK = VarArray(size=[4, n, BC, n, BC], dom={0, 1})  # eqK[i][r1][j1][r2][j2] => The byte values of DeltaK[r1,i,j1] and [r2,i,j2] are equal.

colX = VarArray(size=[n, BC], dom=range(5))  # colX[r][j] = The sum for i in 0..3 of DeltaY[r][i][j]

colSRX = VarArray(size=[n, BC], dom=range(5))  # colSRX; % colSRX[r][j] = The sum for i in 0..3 of SR(DeltaY)[r][i][j]

colK = VarArray(size=[n, BC], dom=range(5))  # colK[r][j] = The sum for i in 0..3 of DeltaK[r][i][j]

DIFF_SX = VarArray(size=[n * BC, n * BC], dom=lambda i, j: {0, 1} if i < j else None)

EQ_SRX = VarArray(size=[n * BC, n * BC], dom=lambda i, j: range(5) if i < j else None)

EQ_Y = VarArray(size=[n * BC, n * BC], dom=lambda i, j: range(5) if i < j else None)

XOR = lambda a, b, c: a + b + c != 1  # regular xor, except 1 xor 1 can be either 0 or 1
XOR2 = lambda a, b, c, eqab, eqac, eqbc: [a + b + c != 1, eqab == 1 - c, eqac == 1 - b, eqbc == 1 - a]  # xor with equivalence propagation

idxa1 = [(J, J // BC, J % BC, (J - KC) // BC, (J - KC) % BC, (J - 1) // BC, (J + BC - 1) % BC) for J in range(BC * n)]
idxa2 = [v for v in idxa1 if v[0] >= KC]


def initKS(J, r1, j1, r2, j2, r3, j3, i, k):
    if J < KC:  # for the first key schedule round
        return Kcomp[r1][j1][i][k] == (deltaK[r1][j1][i] if k == J else 0)
    if J % KC == 0:  # else, for SB positions (for AES 128, corresponds to the first column of DK for each round)
        return Kcomp[r1][j1][i][k] == (deltaK[r3][j3][i + 1] if k == (J // KC) * BC + j1 else Kcomp[r2][j2][i][k])


def auxKS(J, r1, j1, r2, j2, r3, j3, i):
    if J % KC == 0:
        return XOR(deltaK[r2][j2][i], deltaK[r3][j3][(i + 1) % 4], deltaK[r1][j1][i])
    return [
        XOR2(deltaK[r2][j2][i], deltaK[r3][j3][i], deltaK[r1][j1][i], eqK[i][r3][j3][r2][j2], eqK[i][r1][j1][r2][j2], eqK[i][r1][j1][r3][j3]),
        [Kcomp[r1][j1][i][k] == (Kcomp[r2][j2][i][k] * deltaK[r2][j2][i] != Kcomp[r3][j3][i][k] * deltaK[r3][j3][i]) for k in range(NBK)]
    ]


satisfy(
    # the sum to minimize
    Sum(colSRX) + Sum(colK[J // BC][J % BC] for J in range(BC * n) if J % KC == KC - 1) == z,

    # initialisation of the redundant variables
    [
        (
            colX[r][j] == Sum(deltaX[r][j]),
            colK[r][j] == Sum(deltaK[r][j]),
            colSRX[r][j] == Sum(deltaSR[r][j])
        ) for r in range(n) for j in range(BC)
    ],

    # ARK (Add Round Key)
    [XOR(deltaY[r - 1][j][i], deltaK[r][j][i], deltaX[r][j][i]) for r in range(1, n) for j in range(BC) for i in range(4)],

    # MDS property SR (Shift Rows)
    [deltaSR[r][j][i] == deltaX[r][j + i][i] for r in range(n) for j in range(BC) for i in range(4)],

    # MDS property MC (Mix Columns)
    [colSRX[r][j] + Sum(deltaY[r][j]) in {0, 5, 6, 7, 8} for r in range(n - 1) for j in range(BC)],

    # init KS
    [initKS(*v, i, k) for v in idxa1 for i in range(4) for k in range(NBK)],

    # KS (Key Schedule)
    [
        [auxKS(*v, i) for v in idxa2 for i in range(4)],
        [Sum(Kcomp[J // BC][J % BC][i]) + deltaK[J // BC][J % BC][i] != 1 for J in range(KC, n * BC) for i in range(4)]
    ],

    # EQ relations; if (in byte values) DK[r1][i][j1] == DK[r2][i][j2] and DK[r2][i][j2] == DK[r3][i][j3] then DK[r1][i][j1] == DK[r3][i][j3]
    [
        (
            If(  # EQ(a,b) => A=B
                eqK[i][r1][j1][r2][j2],
                Then=deltaK[r1][j1][i] == deltaK[r2][j2][i]
            ),

            eqK[i][r1][j1][r2][j2] == eqK[i][r2][j2][r1][j1],  # symmetry

            If(  # Va=Vb => EQ(a,b)
                [Kcomp[r1][j1][i][k] == Kcomp[r2][j2][i][k] for k in range(NBK)],
                Then=eqK[i][r1][j1][r2][j2] == 1
            ),

            Sum(deltaK[r1][j1][i], deltaK[r2][j2][i], eqK[i][r1][j1][r2][j2]) != 0,  # a+b+EQ(a,b) !=0

            [  # transitivity
                Sum(eqK[i][r1][j1][r3][j3], eqK[i][r1][j1][r2][j2], eqK[i][r2][j2][r3][j3]) != 2 for r3 in range(n) for j3 in range(BC)
            ]
        ) for J1, J2 in combinations(n * BC, 2) if (r1 := J1 // BC, j1 := J1 % BC, r2 := J2 // BC, j2 := J2 % BC) for i in range(4)
    ],

    # Linear MC
    [
        (
            DIFF_SX[J1][J2] == Exist(
                disjunction(
                    deltaSR[r1 - 1][j1][i] != deltaSR[r2 - 1][j2][i],  # different bit values
                    deltaY[r1 - 1][j1][i] != deltaY[r2 - 1][j2][i],  # different after MC (since A==b => MC(A) == MC(B))
                    eqK[i][r1][j1][r2][j2] + deltaX[r1][j1][i] + deltaX[r2][j2][i] == 0,  # MC(SB(A)) xor K1 + MC(SB(B)) xor K2 = 0 and not(EQ(K1, K2))
                    (eqK[i][r1][j1][r2][j2] + deltaK[r1][j1][i] == 2) & (deltaX[r1][j1][i] != deltaX[r2][j2][i])  # MC(SB(A)) xor K != MC(SB(B)) xor K
                ) for i in range(4)
            ),

            EQ_SRX[J1][J2] == Sum(  # Lower bound on the equalities between SR(SB(A)) and SR(SB(B))
                deltaSR[r1 - 1][j1][i] + deltaSR[r2 - 1][j2][i] == 0 for i in range(4)
            ),

            EQ_Y[J1][J2] == Sum(  # Lower bound on the equalities between MC(SB(A)) and MC(SB(B))
                either(
                    both(eqK[i][r1][j1][r2][j2], deltaX[r1][j1][i] + deltaX[r2][j2][i] == 0),
                    deltaY[r1 - 1][j1][i] + deltaY[r2 - 1][j2][i] == 0
                ) for i in range(4)
            )
        ) for J1 in range(BC, n * BC) for J2 in range(J1 + 1, n * BC) if (r1 := J1 // BC, j1 := J1 % BC, r2 := J2 // BC, j2 := J2 % BC)
    ],

    [  # If S(A) != S(B) (in bytes) then MDS Property
        If(
            DIFF_SX[J1][J2],
            Then=EQ_SRX[J1][J2] + EQ_Y[J1][J2] <= 3
        ) for J1 in range(BC, n * BC) for J2 in range(J1 + 1, n * BC)
    ]
)

"""
1) data used in 2016 are : (5,11,128) (5,14,128) (5,16,128) (5,17,128) (7,10,192)
2) auto-adjustment of array indexing is used:
 For example, deltaX[r][j + i][i] is equivalent to deltaX[r][(j + i) % BC][i]
"""

# maximize(
#      Sum(colSRX) + Sum(colK[J // BC, J % BC] for J in range(BC * n) if J % KC == KC - 1)
# )
