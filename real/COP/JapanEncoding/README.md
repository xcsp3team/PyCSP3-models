# Problem JapanEncoding
## Description
There are several popular character encodings in Japan: EUC-JP, SJIS, UTF-8.
If they are mixed into one text file, text information is lost.
Recovering original encodings from a given byte stream is to assign an encoding to each character.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2017 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  0200.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python JapanEncoding.py -data=<datafile.json>
  python JapanEncoding.py -data=<datafile.dzn> -parser=JapanEncoding_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  real, mzn14, mzn17
