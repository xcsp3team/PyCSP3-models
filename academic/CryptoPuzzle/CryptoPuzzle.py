"""
Verbal arithmetic, also known as alphametics, cryptarithmetic, cryptarithm or word addition, is a type of mathematical game
consisting of a mathematical equation among unknown numbers, whose digits are represented by letters of the alphabet.

### Example
  For the Puzzle:
  ```
       S E N D
   +   M O R E
   = M O N E Y
  ```
  a possible solution is:
  ```
       9 5 6 7
   +   1 0 8 5
   = 1 0 6 5 2
  ```

## Data
  Three strings/words (as for example [send,more,money])

## Model
  There are a main variant and a variant involving carry variables.
  You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/CryptoPuzzle/).

  constraints: AllDifferent, Sum

## Execution
  - python CryptoPuzzle.py -data=[string,string,string]
  - python CryptoPuzzle.py -data=[string,string,string] -variant=carry

## Links
  - https://en.wikipedia.org/wiki/Verbal_arithmetic

## Tags
  academic, notebook
"""

from pycsp3 import *

word1, word2, word3 = words = [w.lower() for w in data] if data else ("no", "no", "yes")
n = len(word1)
assert len(word2) == n and len(word3) in {n, n + 1}

# x[i] is the value assigned to the ith letter (if present) of the alphabet
x = VarArray(size=26, dom=lambda i: range(10) if i in alphabet_positions(words) else None)

# auxiliary lists of variables associated with the three words
x1, x2, x3 = [[x[i] for i in reversed(alphabet_positions(word))] for word in words]

satisfy(
    # all letters must be assigned different values
    AllDifferent(x),

    # the most significant letter of each word cannot be equal to 0
    [
        x1[-1] != 0,
        x2[-1] != 0,
        x3[-1] != 0
    ]
)

if not variant():
    satisfy(
        # ensuring the crypto-arithmetic sum
        Sum((x1[i] + x2[i]) * 10 ** i for i in range(n)) == Sum(x3[i] * 10 ** i for i in range(len(x3)))
    )

elif variant("carry"):
    # c[i] is the ith carry
    c = VarArray(size=n + 1, dom={0, 1})

    satisfy(
        # managing the least significant carry
        c[0] == 0,

        # managing the most significant carry
        c[n] == (0 if len(x3) == n else x3[n]),  # NB: the parentheses are required

        # managing remainders
        [(c[i] + x1[i] + x2[i]) % 10 == x3[i] for i in range(n)],

        # managing quotients
        [(c[i] + x1[i] + x2[i]) // 10 == c[i + 1] for i in range(n)]
    )

"""
1) Example of data: (no,no,yes) (two,two,four) (send,more,money) (cross,road,danger) (donald,gerald,robert)
"""
