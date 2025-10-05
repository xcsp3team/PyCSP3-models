"""
This model finds a shortest program to compute a linear combination of variables.
The difficulty is that the program can only use the binary plus and the unary minus.
The symbolic program is linked to a set of examples against which it must conform.
This is one part of a counter-example guided loop, where examples are added when a counter example is found for the generated programs.
The counter-example generation is the other part and not included in this problem, which only does the program generation.
As an example, if the linear combination is -2 * p0 + -1 * p1 + 2 * p2, then a shortest program (among others) might be:
  - x3 = p0 + p0
  - x4 = p1 + x3
  - x5 = p2 + p2
  - x6 = - x4
  - x7 = x5 + x6
  - return x7

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013 Minizinc challenge.
The original MZN model was proposed by Jean-Noel Monette, Uppsala University.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  l2p01.json

## Model
  constraints: AllDifferent, Element, Sum

## Execution
  python LinearToProgram.py -data=<datafile.json>
  python LinearToProgram.py -data=<datafile.dzn> -parser=LinearToProgram_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  realistic, mzn13
"""

from pycsp3 import *

nInputs, nLines, nPlus, coefficients, real_parameters = data or load_json_data("l2p01.json")

nExamples, nLocal = len(real_parameters), 2 * nPlus + (nLines - nPlus)

f = lambda i: sum(2 if j < nPlus else 1 for j in range(i))
intervals = [[0, 1] if i == 0 else list(range(f(i), f(i + 1))) for i in range(nLines)]

max_x_ = 2 * max(max(abs(v) for row in real_parameters for v in row), max(abs(coefficients * real_parameters[s]) for s in range(nExamples)))

L, E = range(nLines), range(nExamples)

line_o = VarArray(size=nLines, dom=range(nInputs, nInputs + nLines))

line_i = VarArray(size=nLocal, dom=range(nInputs + nLines))

x_o = VarArray(size=[nExamples, nLines], dom=range(-max_x_, max_x_ + 1))

x_i = VarArray(size=[nExamples, nLocal], dom=range(-max_x_, max_x_ + 1))

z = Var(dom=range(nInputs, nInputs + nLines))

satisfy(
    # each component is on a different line
    AllDifferent(line_o),

    # ordering of the lines (components use the output of previous lines)
    [line_i[j] < line_o[i] for i in L for j in intervals[i]],

    # computing intermediate variables for examples
    [x_o[e][i] == (x_i[e][lb] + x_i[e][lb + 1] if i < nPlus else -x_i[e][lb]) for e in E for i in L if [lb := min(intervals[i])]],

    # linking the general outputs
    [
        If(
            line_o[i] == z,
            Then=x_o[e][i] == coefficients * real_parameters[e]
        ) for i in L for e in E
    ],

    # linking the general inputs
    [
        If(
            line_i[j] < nInputs,
            Then=x_i[e][j] == real_parameters[e][line_i[j]]
        ) for j in range(nLocal) for e in E
    ],

    # linking the output/input of the intermediate lines
    [
        [
            If(
                line_o[i] == line_i[j],
                Then=x_o[e][i] == x_i[e][j]
            ) for i in L for j in range(nLocal) for e in E
        ],
        [
            If(
                line_o[i] > z,
                Then=line_i[j] == 0
            ) for i in L for j in intervals[i]
        ]
    ],

    # tag(symmetry-breaking)
    [
        # all plus are equivalent
        [line_o[i] < line_o[i + 1] for i in range(nPlus - 1)],

        # all minus are equivalent
        [line_o[i] < line_o[i + 1] for i in range(nPlus, nLines - 1)],

        # plus is commutative
        [line_i[lb] <= line_i[lb + 1] for i in range(nPlus) if [lb := min(intervals[i])]]
    ]
)

minimize(
    z
)

""" Comments
1) Simplification possible for symmetry-breaking by using Increasing
2) one could write: 
 [
        [x_o[s, r] == x_i[s, min(intervals[r])] + x_i[s, min(intervals[r]) + 1] for s in range(nExamples) for r in range(nLines) if r < nPlus],
        [x_o[s, r] == - x_i[s, min(intervals[r])] for s in range(nExamples) for r in range(nLines) if r >= nPlus]
    ],
2) It is now possible to write:
     If(
        i < nPlus,
        Then=x_o[e][i] == x_i[e][lb] + x_i[e][lb + 1],
        Else=x_o[e][i] == -x_i[e][lb]
      )
      for e in E for i in L if [lb := min(intervals[i])]
    ],
   even if the test is not constraint-based (i.e., does not involve any variable of the model)
   but note that all expressions will be built/evaluated (and after that, either the Then or the Else part will be discarded) 
3) Do not write:
 if (lb := min(intervals[i]))
 because if lb is 0, the test returns False
 (but you can write (lb := min(intervals[i]),)
"""
