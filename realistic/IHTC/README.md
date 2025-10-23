# Problem: IHTC

The Integrated Healthcare Timetabling Problem (IHTP), brings together three NP-hard problems and requires the following decisions:
  - (i) the admission date for each patient (or admission postponement to the next scheduling period),
  - (ii) the room for each admitted patient for the duration of their stay,
  - (iii) the nurse for each room during each shift of the scheduling period, and (iv) the operating theater (OT) for each admitted patient.
See ihtc2024.github.io

Important; the model proposed below (by C. Lecoutre) is an abridged version wrt the full problem.

## Data Example
  i01.json

## Model
  constraints: [BinPacking](https://pycsp.org/documentation/constraints/BinPacking), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python IHTC.py -data=<datafile.json>
  python IHTC.py -data=<datafile.json> -parser=IHTC_Converter.py
```

## Links
  - https://ihtc2024.github.io/assets/files/ihtc2024_problem_specification.pdf
  - https://ihtc2024.github.io/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
