# Problem: IHTC24K

The Integrated Healthcare Timetabling Problem (IHTP), brings together three NP-hard problems and requires the following decisions:
  - (i) the admission date for each patient (or admission postponement to the next scheduling period),
  - (ii) the room for each admitted patient for the duration of their stay,
  - (iii) the nurse for each room during each shift of the scheduling period, and (iv) the operating theater (OT) for each admitted patient.
See ihtc2024.github.io

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
The original mzn model by Lucas Kletzander -- No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  i02.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python IHTC24K.py -data=<datafile.json>
  python IHTC24K.py -data=<datafile.json> -parser=IHTC24K_ParserZ.py
```

## Links
  - https://ihtc2024.github.io/assets/files/ihtc2024_problem_specification.pdf
  - https://ihtc2024.github.io/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
