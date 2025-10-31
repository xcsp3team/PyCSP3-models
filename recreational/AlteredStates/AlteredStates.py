"""
From JaneStreet:
    Enter letters into a n×n grid above to achieve the highest score you can.
    You earn points for each of the 50 U.S. states present in your grid. Note that:
      - states can be spelled by making King’s moves from square to square
      - the score for a state is its length (main variant)
      - if a state appears multiple times in your grid, it only scores once

## Data
  a number n

## Model
  constraints: Element, Lex, Sum

## Execution
  python AlteredStates.py -data=number
  python AlteredStates.py -data=number -variant=bis

## Links
  - https://www.janestreet.com/puzzles/altered-states-index/
  - https://www.janestreet.com/puzzles/altered-states-2-index/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, janestreet, xcsp25
"""

from pycsp3 import *
from pycsp3.classes.main.annotations import ValHeuristic
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

assert not variant() or variant("bis")

n = data or 5

states = [
    ("Alabama", 5_024_279),  # 0
    ("Alaska", 733_391),  # 1
    ("Arizona", 7_151_502),  # 2
    ("Arkansas", 3_011_524),  # 3
    ("California", 39_538_223),  # 4
    ("Colorado", 5_773_714),  # 5
    ("Connecticut", 3_605_944),  # 6
    ("Delaware", 989_948),  # 7
    ("Florida", 21_538_187),  # 8
    ("Georgia", 10_711_908),  # 9
    ("Hawaii", 1_455_271),  # 10
    ("Idaho", 1_839_106),  # 11
    ("Illinois", 12_812_508),  # 12
    ("Indiana", 6_785_528),  # 13
    ("Iowa", 3_190_369),  # 14
    ("Kansas", 2_937_880),  # 15
    ("Kentucky", 4_505_836),  # 16
    ("Louisiana", 4_657_757),  # 17
    ("Maine", 1_362_359),  # 18
    ("Maryland", 6_177_224),  # 19
    ("Massachusetts", 7_029_917),  # 20
    ("Michigan", 10_077_331),  # 21
    ("Minnesota", 5_706_494),  # 22
    ("Mississippi", 2_961_279),  # 23
    ("Missouri", 6_154_913),  # 24
    ("Montana", 1_084_225),  # 25
    ("Nebraska", 1_961_504),  # 26
    ("Nevada", 3_104_614),  # 27
    ("NewHampshire", 1_377_529),  # 28
    ("NewJersey", 9_288_994),  # 29
    ("NewMexico", 2_117_522),  # 30
    ("NewYork", 20_201_249),  # 31
    ("NorthCarolina", 10_439_388),  # 32
    ("NorthDakota", 779_094),  # 33
    ("Ohio", 11_799_448),  # 34
    ("Oklahoma", 3_959_353),  # 35
    ("Oregon", 4_237_256),  # 36
    ("Pennsylvania", 13_002_700),  # 37
    ("RhodeIsland", 1_097_379),  # 38
    ("SouthCarolina", 5_118_425),  # 39
    ("SouthDakota", 886_667),  # 40
    ("Tennessee", 6_910_840),  # 41
    ("Texas", 29_145_505),  # 42
    ("Utah", 3_271_616),  # 43
    ("Vermont", 643_077),  # 44
    ("Virginia", 8_631_393),  # 45
    ("Washington", 7_705_281),  # 46
    ("WestVirginia", 1_793_716),  # 47
    ("Wisconsin", 5_893_718),  # 48
    ("Wyoming", 576_851)  # 49
]
names, populations = zip(*states)
lengths = [len(name) for name in names]
nStates, M = len(states), max(lengths)

symmetries = [[i * n + j for i, j in S] for sym in TypeSquareSymmetry if (S := flatten(sym.apply_on(n), keep_tuples=True))]

words = [alphabet_positions(name.lower()) for name in names]  # words converted to numbers (0 to 25)

T = [(i * n + j, (i + k) * n + (j + p)) for i in range(n) for j in range(n) for k in [-1, 0, 1] for p in [-1, 0, 1]
     if 0 <= i + k < n and 0 <= j + p < n and (k, p) != (0, 0)]

# x[ij] is the letter (index) in cell whose index is ij
x = VarArray(size=n * n, dom=range(26))

# y[k] is 1 if the kth state is present in the matrix
y = VarArray(size=nStates, dom={0, 1})

# z[k][q] is the (flat) cell index in x of the qth letter of the kth state, or 0 if the state is not present
z = VarArray(size=[nStates, M], dom=lambda k, q: range(n * n) if q < lengths[k] else None)

satisfy(
    # ensuring the coherence of putting or not the states in the grid
    [
        If(
            y[k] == 0,
            Then=[z[k][q] == 0 for q in Q],  # we force 0 to avoid symmetries  z[k] == 0,
            Else=[
                [x[z[k][q]] == words[k][q] for q in Q] if not variant() else Sum(x[z[k][q]] != words[k][q] for q in Q) <= 1,  # ensuring the name is present
                [(z[k][q], z[k][q + 1]) in T for q in Q[:-1]]  # ensuring connectedness of letters
            ]
        ) for k in range(nStates) if (Q := range(lengths[k]))
    ],

    # tag(symmetry-breaking)
    [x <= x[symmetry] for symmetry in symmetries]
)

if not variant():
    maximize(
        y * lengths
    )

elif variant("bis"):
    maximize(
        y * populations
    )

# annotate(
#     valHeuristic=ValHeuristic().static(y, order=[1, 0])
# )

""" Comments
1) Note that:
     [x <= x[symmetry] for symmetry in symmetries]
  is a shorter way of writing:
    LexIncreasing(
        x,
        [x[row] for row in symmetry]
     ) for symmetry in symmetries
2) with z[k] == 0, l'instance xml est différente et ACE ne reconnait pas la dcecomposition possible (et c'est tres inefficace)
3) the table constraint involved in the 'If' expression needs some kind of reification, which is handled (when compiling) by building a ternary constraint 
   in order to make a link with the condition of the 'If' expression.
4) Data used for the 2025 competition are: [2, 3, 4, 5, 6, 8, 10, 12, 15]
"""

# [Table(scope=(z[k][q], z[k][q + 1]), supports=T) for q in Q[:-1]],

# satisfy(
#     # tag(special)
#     [
#         y[37] == 1,  # Pensylvania
#         # y[18:26] == 1,  # M states
#         y[43] == 1,
#         y[5] == 1,
#         y[2] == 1,
#         y[30] == 1,
#         y[4] == 0,  # no cal
#     ]
# )
