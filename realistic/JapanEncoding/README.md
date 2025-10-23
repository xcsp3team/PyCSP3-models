# Problem: JapanEncoding

Japan Encoding.

Description taken from the journal paper cited below:
    The JP-encoding problem is to recover the original encoding of a stream of Japanese text where several encodings might have been mixed, say by accident.
    The considered encodings are ASCII, EUC-JP, SJIS, and UTF-8. An array of bytes is given and the goal is to assign to each byte its encoding
    in order to maximise the sum of the likelihoods of each byte appearing in the assigned encoding.
    The encodings may use different numbers of bytes to represent a given character.
    For example, ASCII always uses one byte, but UTF-8 may use from one to four bytes depending on the encoded character.
    In addition, each encoding defines ranges of possible values for the byte of each position.
    For example, an ASCII byte can only have a value from 0 to 127, and a UTF-8 character on two bytes must have the first byte from 194 to 223
    and the second byte from 128 to 191.


The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2017 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  0100.json

## Model
  constraints: [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python JapanEncoding.py -data=<datafile.json>
  python JapanEncoding.py -data=<datafile.dzn> -parser=JapanEncoding_ParserZ.py
```

## Links
  - https://link.springer.com/article/10.1007/s10601-017-9270-5
  - https://www.jair.org/index.php/jair/article/view/17032
  - https://www.minizinc.org/challenge/2017/results/

## Tags
  realistic, mzn14, mzn17
