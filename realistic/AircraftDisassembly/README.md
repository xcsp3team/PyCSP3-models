# Problem: AircraftDisassembly

Aircraft Disassembly Scheduling

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
The original mzn model by Allen Zhon (No Licence was explicitly mentioned - MIT Licence assumed), while being inspired by:
  - the CP Optimizer [model](https://github.com/cftmthomas/AircraftDisassemblyScheduling) for Aircraft Disassembly Scheduling
  - the MiniZinc [model](https://github.com/youngkd/MSPSP-InstLib) for Multi-Skill Project Scheduling Problem

## Data Example
  600-01.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python AircraftDisassembly.py -data=<datafile.json>
  python AircraftDisassembly.py -data=<datafile.dzn> -parser=AircraftDisassembly_ParserZ.py
```

## Links
  - https://link.springer.com/chapter/10.1007/978-3-031-60599-4_13
  - https://github.com/cftmthomas/AircraftDisassemblyScheduling
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
