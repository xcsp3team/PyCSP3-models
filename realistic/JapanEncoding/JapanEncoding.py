"""
Japan Encoding.

Description taken from the journal paper cited below:
    The JP-encoding problem, introduced in the MiniZinc Challenge 2014, is to recover the
    original encoding of a stream of Japanese text where several encodings might have been
    mixed, say by accident. The considered encodings are ASCII, EUC-JP, SJIS, and UTF-8.
    An array of bytes is given and the goal is to assign to each byte its encoding in order to
    maximise the sum of the likelihoods of each byte appearing in the assigned encoding. The
    encodings may use different numbers of bytes to represent a given character. For example,
    ASCII always uses one byte, but UTF-8 may use from one to four bytes depending on the
    encoded character. In addition, each encoding defines ranges of possible values for the byte
    of each position. For example, an ASCII byte can only have a value from 0 to 127, and a
    UTF-8 character on two bytes must have the first byte from 194 to 223 and the second byte
    from 128 to 191


The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2017 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  0100.json

## Model
  constraints: Sum

## Execution
  python JapanEncoding.py -data=<datafile.json>
  python JapanEncoding.py -data=<datafile.dzn> -parser=JapanEncoding_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-017-9270-5
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn14, mzn17
"""

from pycsp3 import *

stream = data or load_json_data("0100.json")

n = len(stream)

N = range(n)

# three tables of scores ; tables have -log(probability of appearance) * 10 for each encoding

scoreSJIS = [
    135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 57, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135,
    135, 74, 135, 128, 119, 135, 100, 135, 135, 96, 96, 112, 104, 106, 92, 106, 107, 97, 92, 99, 95, 98, 106, 107, 103, 97, 101, 105, 135, 135, 111, 135, 119,
    65, 46, 45, 64, 75, 74, 79, 78, 71, 74, 79, 76, 71, 79, 59, 64, 81, 78, 70, 67, 80, 81, 70, 82, 69, 81, 75, 72, 62, 60, 73, 70, 76, 79, 75, 66, 77, 75, 78,
    73, 77, 43, 43, 79, 54, 68, 68, 61, 73, 67, 80, 66, 69, 53, 51, 72, 73, 68, 74, 71, 77, 80, 77, 135, 77, 28, 11, 51, 75, 73, 69, 69, 51, 47, 49, 49, 44, 49,
    41, 47, 44, 48, 48, 47, 50, 46, 45, 48, 63, 76, 75, 79, 74, 68, 63, 73, 50, 67, 40, 80, 45, 79, 56, 71, 59, 42, 45, 55, 67, 49, 68, 58, 69, 53, 65, 54, 69,
    45, 57, 50, 64, 60, 65, 54, 67, 44, 49, 58, 66, 47, 58, 74, 43, 47, 43, 59, 43, 45, 62, 62, 40, 45, 60, 72, 71, 69, 72, 68, 61, 80, 62, 68, 72, 68, 70, 75,
    51, 66, 67, 61, 47, 56, 59, 61, 62, 53, 53, 47, 51, 43, 49, 60, 74, 60, 83, 74, 47, 47, 76, 71, 78, 82, 77, 83, 80, 81, 70, 67, 67, 135, 135, 135
]
scoreEUCJP = [
    135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 57, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135,
    135, 74, 135, 128, 119, 135, 100, 135, 135, 96, 96, 112, 104, 106, 92, 106, 107, 97, 92, 99, 95, 98, 106, 107, 103, 97, 101, 105, 135, 135, 111, 135, 119,
    135, 112, 114, 100, 108, 102, 135, 113, 121, 110, 124, 135, 111, 106, 111, 111, 100, 135, 114, 109, 112, 124, 135, 135, 124, 119, 128, 128, 121, 128, 135,
    135, 135, 94, 128, 102, 104, 95, 113, 97, 108, 90, 124, 124, 99, 101, 95, 90, 105, 135, 93, 99, 94, 108, 128, 113, 135, 124, 117, 135, 135, 135, 135, 135,
    135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135,
    135, 135, 28, 41, 44, 11, 50, 45, 72, 55, 64, 57, 42, 45, 54, 65, 46, 49, 49, 51, 48, 50, 48, 54, 41, 45, 45, 52, 44, 48, 45, 49, 39, 43, 50, 51, 43, 49,
    53, 40, 43, 41, 50, 34, 36, 48, 45, 38, 43, 53, 66, 62, 66, 61, 62, 49, 50, 59, 62, 62, 63, 63, 68, 50, 63, 63, 58, 46, 55, 57, 59, 58,
    52, 50, 46, 49, 43, 48, 58, 63, 58, 73, 67, 46, 46, 70, 68, 58, 66, 71, 73, 72, 74, 66, 61, 58, 135
]
scoreUTF8 = [
    139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 61, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139,
    139, 78, 139, 132, 123, 139, 104, 139, 139, 100, 100, 116, 108, 110, 96, 110, 111, 101, 96, 103, 99, 102, 110, 111, 107, 101, 105, 109, 139, 139, 115, 139,
    139, 139, 116, 118, 104, 112, 107, 139, 117, 125, 114, 128, 139, 115, 110, 115, 115, 104, 139, 118, 113, 116, 128, 139, 139, 128, 123, 132, 132, 125, 132,
    139, 139, 139, 98, 132, 107, 108, 99, 117, 101, 112, 95, 128, 128, 103, 105, 99, 94, 109, 139, 97, 103, 98, 112, 132, 117, 139, 128, 121, 139, 139, 139,
    139, 139, 36, 17, 27, 51, 42, 55, 47, 54, 41, 40, 49, 38, 42, 47, 64, 48, 53, 52, 49, 45, 56, 51, 56, 46, 58, 50, 58, 52, 57, 51, 65, 46, 51, 53, 63, 48,
    54, 54, 44, 48, 45, 54, 45, 46, 61, 53, 42, 47, 53, 61, 63, 57, 61, 63, 62, 62, 48, 59, 45, 53, 39, 57, 49, 57, 139, 139, 139, 132, 139, 139, 139, 139, 139,
    139, 139, 139, 139, 139, 118, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 68, 14, 42, 36, 40, 44, 44, 47,
    139, 139, 139, 139, 139, 40, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139
]


def not_in(d):
    return any(all(stream[i] not in range(a, b) for a, b in t) for i, k in d.items() if (t := k if isinstance(k, list) else [k]))


ASCII, EUCJP, SJIS, UTF8, UNKNOWN = Encodings = range(5)
A, E1, E2, S11, S21, S22, U21, U22, U31, U32, U33, U41, U42, U43, U44, Ukn = ByteLabels = range(16)

# y[i] is the byte status of the ith byte
y = VarArray(size=n, dom=ByteLabels)

# x[i] is the encoding of the ith byte
x = VarArray(size=n, dom=Encodings)

# cs[i] is 1 if the ith byte starts a character
cs = VarArray(size=n, dom={0, 1})

# z is the number of unknown bytes
z = Var(dom=range(n + 1))

satisfy(

    # ensuring correspondence between encodings and byte labels
    (
        [(x[i] == ASCII) == (y[i] == A) for i in N],
        [If(x[i] == EUCJP, Then=y[i] in (E1, E2)) for i in N],
        [If(x[i] == SJIS, Then=y[i] in (S11, S21, S22)) for i in N],
        [If(x[i] == UTF8, Then=y[i] in (U21, U22, U31, U32, U33, U41, U42, U43, U44)) for i in N],
        [(x[i] == UNKNOWN) == (y[i] == Ukn) for i in N]
    ),

    # about ASCII (1 byte)
    (
        [y[i] != A for i in N if stream[i] >= 128],
        [If(y[i] == A, Then=cs[i]) for i in N]
    ),

    # about UTF8 (2 bytes) while paying attention to ranges C2-DF, 80-BF
    (
        y[-1] != U21,
        [y[i] != U21 for i in N[: - 1] if not_in({i: (194, 224), i + 1: (128, 192)})],
        y[0] != U22,
        [Iff(y[i] == U21, y[i + 1] == U22) for i in N[: - 1]],
        [If(y[i] == U21, Then=cs[i] == 1) for i in N],
        [If(y[i] == U22, Then=cs[i] == 0) for i in N]
    ),

    # about UTF8 (3 bytes) while paying attention to ranges E0-EF, 80-BF, 80-BF
    (
        [y[-1] != U31, y[-2] != U31],
        [y[i] != U31 for i in N[:- 2] if not_in({i: (224, 240), i + 1: (128, 192), i + 2: (128, 192)})],
        y[0] != U32,
        [(y[i] == U31) == (y[i + 1] == U32) for i in N[:-1]],
        [y[0] != U33, y[1] != U33],
        [Iff(y[i] == U31, y[i + 2] == U33) for i in N[:-2]],
        [If(y[i] == U31, Then=cs[i] == 1) for i in N],
        [If(y[i] in (U32, U33), Then=cs[i] == 0) for i in N]
    ),

    # about UTF8 (4 bytes) while paying attention to ranges F0-F7, 80-BF, 80-BF, 80-BF
    (
        [y[-1] != U41, y[-2] != U41, y[-3] != U41],
        [y[i] != U41 for i in range(n - 3) if not_in({i: (240, 248), i + 1: (128, 192), i + 2: (128, 192), i + 3: (128, 192)})],
        y[0] != U42,
        [Iff(y[i] == U41, y[i + 1] == U42) for i in N[: - 1]],
        [y[0] != U43, y[1] != U43],
        [Iff(y[i] == U41, y[i + 2] == U43) for i in N[: - 2]],
        [y[0] != U44, y[1] != U44, y[2] != U44],
        [iff(y[i] == U41, y[i + 3] == U44) for i in N[: - 3]],
        [If(y[i] == U41, Then=cs[i] == 1) for i in N],
        [If(y[i] in (U42, U43, U44), Then=cs[i] == 0) for i in N]
    ),

    # about EUC-JP (2 bytes) while paying attention to ranges (A1-A8, AD, B0-F4, F9-FC), (A1-FE)
    (
        [y[i] != E1 for i in N if not_in({i: [(161, 169), (173, 174), (176, 245), (249, 253)], i + 1: (161, 255)})],
        y[0] != E2,
        [Iff(y[i] == E1, y[i + 1] == E2) for i in N[:-1]],
        [If(y[i] == E1, Then=cs[i] == 1) for i in N],
        [If(y[i] == E2, Then=cs[i] == 0) for i in N]
    ),

    # about SJIS (1 byte) while paying attention to range A1-DF
    (
        [y[i] != S11 for i in N if stream[i] not in range(161, 224)],
        [If(y[i] == S11, Then=cs[i] == 1) for i in N]
    ),

    # about SJIS (2 bytes) while paying attention to ranges (81-9F, E0-FC), (40-7E, 80-FC)
    (
        y[-1] != S21,
        [y[i] != S21 for i in N[:-1] if not_in({i: [(129, 160), (224, 253)], i + 1: [(64, 127), (128, 253)]})],
        y[0] != S22,
        [iff(y[i] == S21, y[i + 1] == S22) for i in N[:- 1]],
        [If(y[i] == S21, Then=cs[i] == 1) for i in N],
        [If(y[i] == S22, Then=cs[i] == 0) for i in N]
    ),

    # about unknown characters
    (
        [If(y[i] == Ukn, Then=cs[i]) for i in N],
        Count(x, value=UNKNOWN) == z
    )
)

minimize(
    Sum(
        (x[i] == EUCJP) * scoreEUCJP[b]
        + (x[i] == SJIS) * scoreSJIS[b]
        + (x[i] == UTF8) * scoreUTF8[b]
        for i, b in enumerate(stream)
    )
    + 1000 * z
)

"""
1) (x[i] == ASCII) == (y[i] == A) 
 can be equivalently written:
  iff(x[i] == ASCII,  y[i] == A) 
"""
