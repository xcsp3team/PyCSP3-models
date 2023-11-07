# Problem SuperNumber
## Description
See https://www.logisch-gedacht.de/logikraetsel/10stellige-zahl

We are looking for the 10-digit number which satisfies the following conditions:
- all digits from 0-9 occur exactly once
- the first 2 digits are divisible by 2
- the first 3 digits are divisible by 3
- ...
- the first 10 digits are divisible by 10

Using divisibility rules (https://en.wikipedia.org/wiki/Divisibility_rule) allows us
to use less expensive operations (constraints), but a less compact model

## Data
all integrated (single instance)

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python3 SuperNumber.py
  python3 SuperNumber.py -variant=rules
```

## Links
 - https://www.logisch-gedacht.de/logikraetsel/10stellige-zahl

## Tags
  single
