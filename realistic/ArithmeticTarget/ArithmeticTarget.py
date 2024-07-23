"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Kelvin Davis, under the MIT Licence.

## Data Example
  0814.json

## Model
  constraints: AllDifferent, Count, Element

## Execution
  python ArithmeticTarget.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
"""

from pycsp3 import *

numbers, target = data

n = len(numbers)
m = 2 * n  # - 1

M = range(1, m)
VAL, ADD, SUB, MUL, DIV, NO = Tokens = range(6)

# x[i] is the token associated with the ith node
x = VarArray(size=m, dom=lambda i: {-1} if i == 0 else Tokens)

# left[i] is the left child (or 0 if none) of the ith node
left = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# right[i] is the right child (or 0 if none) of the ith node
right = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# lowest[i] is the lowest descendant of the ith node
lowest = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# highest[i] is the highest descendant of the ith node
highest = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# index[i] is the index of the number associated with the ith node
index = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(n + 1))

# leaf[i] is 1 if the ith node is a leaf
leaf = VarArray(size=m, dom={0, 1})

# parent[i] is 1 if the ith node is a parent
parent = VarArray(size=m, dom={0, 1})

# unused[i] is the ith element is unused
unused = VarArray(size=m, dom={0, 1})

# the tree depth
depth = Var(range(1, 2 * n))

# z1[i] is the value associated with the ith node
z1 = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(10 * target + 1))

# z2 is the number of used nodes
z2 = Var(range(1, n + 1))

satisfy(
    # ensuring that the special value 0 appears n-1 times
    Count(within=index, value=0) == n - 1,

    # ensuring all indexes of numbers are different (except for the special value 0)
    AllDifferent(index, excepting=0),

    # ensuring that the tree has n leaves
    Count(within=x, value=VAL) == n,

    # computing the tree depth
    depth == highest[1],

    # computing the number of unused nodes
    2 * z2 - 1 == depth,

    # determining leaves
    [
        leaf[i] == conjunction(
            x[i] == VAL,
            left[i] == 0,
            right[i] == 0,
            highest[i] == i,
            lowest[i] == i,
            index[i] != 0
        ) for i in M
    ],

    # determining parents
    [
        parent[i] == conjunction(
            x[i] not in (VAL, NO),
            x[left[i]] != NO,
            x[right[i]] != NO,
            left[i] == i + 1,
            right[i] > left[i],
            right[i] == highest[left[i]] + 1,
            lowest[i] == i,
            highest[i] == highest[right[i]],
            index[i] == 0
        ) for i in M
    ],

    # determining unused elements
    [
        unused[i] == conjunction(
            x[i] in (NO, VAL),
            left[i] == 0,
            right[i] == 0,
            If(x[i] == VAL, Then=index[i] != 0),
            If(x[i] == NO, Then=index[i] == 0),
            lowest[i] == 0,
            highest[i] == 0
        ) for i in M
    ],

    # constraining leaves, parents and unused elements
    [
        If(
            i <= depth,
            Then=leaf[i] | parent[i],
            Else=unused[i]
        ) for i in M
    ],

    # computing values associated with all elements
    [
        Match(
            x[i],
            Cases={
                VAL: z1[i] == numbers[index[i]],
                ADD: z1[i] == z1[left[i]] + z1[right[i]],
                SUB: z1[i] == z1[left[i]] - z1[right[i]],
                MUL: z1[i] == z1[left[i]] * z1[right[i]],
                DIV: z1[i] * z1[right[i]] == z1[left[i]],
                NO: z1[i] == 0}
        ) for i in M
    ],

    # tag(symmetry-breaking)
    [
        # associativity
        [
            Match(
                x[i],
                Cases={
                    ADD: x[left[i]] != ADD,
                    MUL: x[left[i]] != MUL,
                    SUB: x[left[i]] != SUB}
            ) for i in M
        ],

        # identity
        [
            [If(x[i] == ADD, Then=[z1[left[i]] != 0, z1[right[i]] != 0]) for i in M],
            [If(x[i] == MUL, Then=[z1[left[i]] != 1, z1[right[i]] != 1]) for i in M]
        ],

        # symmetry of Addition and Multiplication
        [If(x[i] in (ADD, MUL), Then=x[left[i]] <= x[right[i]]) for i in M],

        # distributivity of multiplication
        [
            If(
                x[i] in (ADD, SUB), x[left[i]] == MUL, x[right[i]] == MUL,
                Then=[
                    z1[left[left[i]]] != z1[left[right[i]]],
                    z1[left[left[i]]] != z1[right[right[i]]],
                    z1[right[left[i]]] != z1[left[right[i]]],
                    z1[right[left[i]]] != z1[right[right[i]]]]
            ) for i in M
        ],

        # distributivity of division
        [
            If(
                x[i] in (ADD, SUB), x[left[i]] == DIV, x[right[i]] == DIV,
                Then=z1[right[left[i]]] != z1[right[right[i]]]
            ) for i in M
        ],

        # conditions wrt operations Add and Mul
        [
            (
                If(x[i] == ADD, x[right[i]] == VAL, Then=x[left[i]] == VAL),
                If(x[i] == MUL, x[right[i]] == VAL, Then=x[left[i]] == VAL),
                If(x[i] == ADD, x[left[i]] == VAL, x[right[i]] == VAL, Then=index[left[i]] < index[right[i]]),
                If(x[i] == MUL, x[left[i]] == VAL, x[right[i]] == VAL, Then=index[left[i]] < index[right[i]]),
                If(x[i] == ADD, x[left[i]] == VAL, x[right[i]] == ADD, x[left[right[i]]] == VAL, Then=index[left[i]] < index[left[right[i]]]),
                If(x[i] == MUL, x[left[i]] == VAL, x[right[i]] == MUL, x[left[right[i]]] == VAL, Then=index[left[i]] < index[left[right[i]]])
            ) for i in M
        ],

        # all numbers with the same value should be assigned in sorted order
        [
            If(
                x[i] == VAL, x[j] == VAL, numbers[index[i]] == numbers[index[j]],
                Then=index[i] < index[j]
            ) for i, j in combinations(M, 2)
        ],

        # sorting nodes of equivalent value
        [If(z1[i] == z1[j], Then=x[i] >= x[j]) for i, j in combinations(M, 2)]
    ]
)

minimize(
    10 * abs(z1[1] - target) + z2
)

""" Comments
0) In complex expressions (for example, If), it is not always possible to write something like:
    x[i] in (ADD, SUB)
  Instead, one should write the safer expression: 
    x[i].among(ADD,SUB)
 This is because the operator 'in' cannot be redefined (and it is then quite technical to manage it for side-effects statements)
 Currently, if we write:
    [If(x[i].among(ADD, MUL), Then=x[left[i]] <= x[right[i]]) for i in M],
  instead of:
    [If(x[i] in (ADD, MUL), Then=x[left[i]] <= x[right[i]]) for i in M],
  a problem occurs because the test only contains a single test (and this is currently not handled).

1) [(x[i] != DIV) | (z1[i] * z1[right[i]] == z1[left[i]]) for i in M],
 is posted instead of the problematic (div by zero)
   [(x[i] != DIV) | ((z1[right[i]] != 0) & (z1[i] == z1[left[i]] // z1[right[i]]) & (z1[left[i]] % z1[right[i]] == 0)) for i in M], 
   
2) Other possible manners of posting constraints are:
    [leaf[i] == (x[i] == VAL) & (left[i] == 0) & (right[i] == 0) & (highest[i] == i) & (lowest[i] == i) & (index[i] != 0) for i in M],
    
    [(x[i] != ADD) | (x[left[i]] != VAL) | (x[right[i]] != VAL) | (index[left[i]] < index[right[i]]) for i in M],
    [(x[i] != MUL) | (x[left[i]] != VAL) | (x[right[i]] != VAL) | (index[left[i]] < index[right[i]]) for i in M],
    [(x[i] != ADD) | (x[left[i]] != VAL) | (x[right[i]] != ADD) | (x[left[right[i]]] != VAL) | (index[left[i]] < index[left[right[i]]])
     for i in M],
    [(x[i] != MUL) | (x[left[i]] != VAL) | (x[right[i]] != MUL) | (x[left[right[i]]] != VAL) | (index[left[i]] < index[left[right[i]]])
     for i in M]
    
    # symmetry of Addition and Multiplication
    [((x[i] != ADD) & (x[i] != MUL)) | (x[left[i]] <= x[right[i]]) for i in range(1, m)],
     
    # distributivity of division
    [((x[i] != ADD) & (x[i] != SUB)) | (x[left[i]] != DIV) | (x[right[i]] != DIV) | (z1[right[left[i]]] != z1[right[right[i]]]) for i in M],
    
    # all numbers with the same value should be assigned in sorted order
    [(x[i] != VAL) | (x[j] != VAL) | (numbers[index[i]] != numbers[index[j]]) | (index[i] < index[j]) for i, j in combinations(M, 2)],
    
    # computing values associated with all elements
    [
        [(x[i] != VAL) | (z1[i] == numbers[index[i]]) for i in M],
        [(x[i] != ADD) | (z1[i] == z1[left[i]] + z1[right[i]]) for i in M],
        [(x[i] != SUB) | (z1[i] == z1[left[i]] - z1[right[i]]) for i in M],
        [(x[i] != MUL) | (z1[i] == z1[left[i]] * z1[right[i]]) for i in M],
        [(x[i] != DIV) | (z1[i] * z1[right[i]] == z1[left[i]]) for i in M],
        [(x[i] != NO) | (z1[i] == 0) for i in M]
    ],
    
3) For the instance 814, one solution (chuffed) is: 
    x == [-1, MUL, ADD, VAL, MUL, VAL, VAL, ADD, VAL, VAL, NO, NO, NO, VAL, VAL, VAL],
    left == [-1, 2, 3, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
    right == [-1, 7, 4, 0, 6, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0],
    lowest == [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0],
    highest == [-1, 9, 6, 3, 6, 5, 6, 9, 8, 9, 0, 0, 0, 0, 0, 0],
    #  indexes == [-1, 0, 0, 2, 0, 7, 8, 0, 3, 6, 0, 0, 0, 1, 4, 5],
    z2 == 5,
    z1 == [-1, 814, 74, 2, 72, 8, 9, 11, 4, 7, 0, 0, 0, 1, 6, 6],
  but indexes is not valid in the PyCSP3 model (there is an offset by 1)  

4)  ACE is slow when decomposing (so, needs -di=0)
"""
