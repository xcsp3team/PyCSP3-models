"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
The original MZN model was proposed by David Gerault, under the MIT Licence.

## Data
  Two integers (n,nr)

## Model
  constraints: Sum

## Execution
  python Speck.py -data=[number,number]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-031-30872-7_10
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  academic, mzn23
"""

from pycsp3 import *

n, nr = data or (16, 2)  # word size (n) and number of rounds (nr)

# L[i][j] is the left value of the jth bit in the ith round
L = VarArray(size=[nr + 1, n], dom={0, 1})

# R[i][j] is the right value of the jth bit in the ith round
R = VarArray(size=[nr + 1, n], dom={0, 1})

# p[i] is the probability value associated with the ith round
p = VarArray(size=nr, dom=range(n + 1))

# cd[i][j] is the carry difference for the jth bit of the ith round
cd = VarArray(size=[nr, n], dom={0, 1})

# z is the objective value
z = Var(range(n * 4 + 1))

# auxiliary arrays
lr = 2 if n == 16 else 3  # left rotation value
rr = 7 if n == 16 else 8  # right rotation value
L_rot = [[R[i][(j + lr) % n] for j in range(n)] for i in range(nr)]
R_rot = [[L[i][(n + j - rr) % n] for j in range(n)] for i in range(nr)]


def modular_addition_word(i):
    a, b, c, d = R_rot[i], R[i], L[i + 1], cd[i]
    return (
        d[-1] == 0,

        [xor(a[j], b[j], c[j], d[j]) == 0 for j in range(n)],

        [
            If(
                AllEqual(a[j], b[j], c[j]),
                Then=AllEqual(a[j], b[j], c[j], d[j - 1])
            ) for j in range(1, n)
        ],
        [p[i] == Sum(NotAllEqual(a[j], b[j], c[j], d[j], d[j - 1]) for j in range(1, n))]
    )


satisfy(
    # computing the objective value
    z == Sum(p),

    # ensuring non-zero difference at first round
    Sum(L[0] + R[0]) > 0,

    # round function
    [
        [R[i + 1][j] == L[i + 1][j] ^ L_rot[i][j] for i in range(nr) for j in range(n)],

        # modular addition word
        [modular_addition_word(i) for i in range(nr)]
    ]
)

minimize(
    # minimizing the summed probability values
    z
)

""" Comments
1) Data used in 2023 are: (16,2), (16,4), (64,5), (64,8), (64, 19)
"""
