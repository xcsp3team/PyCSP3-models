"""
Airport Check-in Counter Allocation Problem (ACCAP) with fixed opening/closing times.

Airports have a specific set of check-in counters available for common use by multiple airlines throughout the day.
Airlines have predetermined start and end times for their flight check-in operations before their departure times.
Each flight operates within a fixed time interval during which the check-in must remain open.
Given the number of airlines, their respective flights, the start times for check-in (x),
the required counter capacity (requirement), and the check-in duration (duration),
the objective is to allocate flights (check-ins) to counters (y, indicating the tarting counter index) in a way
that minimizes the maximum number of counters used throughout the day (z).
Simultaneously, the goal is to cluster flights from the same airline together
in the same check-in area, achieving this by minimizing the sum of the total distances (d)
between the counters of each pair of flights from the same airline.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03.json

## Model
  constraints: NoOverlap, Sum

## Execution
  python ACCAP_z.py -data=<datafile.json>
  python ACCAP_z.py -data=<datafile.dzn> -parser=ACCAP_ParserZ.py
  python ACCAP.py -data=<datafile.json> -parser=ACCAP_Converter.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn19, mzn22, mzn24
"""

from pycsp3 import *

flights, airlines = data
durations, requirements, x = zip(*flights)  # requirements in terms of numbers of counters; x stands for starts
nFlights, nAirlines, nCounters = len(flights), len(airlines), sum(requirements)

# y[i] is the first counter (index) of the series required by the ith flight
y = VarArray(size=nFlights, dom=range(nCounters))

# d[a] is the maximal distance between two flights of the airline a
d = VarArray(size=nAirlines, dom=range(nCounters))

# z is the number of used counters
z = Var(dom=range(max(requirements), nCounters + 1))

satisfy(
    # ensuring no counter is shared
    NoOverlap(
        origins=(x, y),
        lengths=(durations, requirements)
    ),

    # computing the number of used counters
    [y[i] + requirements[i] <= z for i in range(nFlights)],

    # computing the maximal distance between two flights of the same airline
    [
        Sum(
            y[i], -y[j], -d[a]
        ) <= 1 - requirements[i] for a in range(nAirlines) for i in airlines[a] for j in airlines[a] if i != j
    ]
)

minimize(
    Sum(d) + z
)

"""
1) Note that:
 Sum(y[i], -y[j], -d[a]) <= 1 - requirements[i] 
   is equivalent to:
 y[i] + (requirements[i] - 1) - y[j] <= d[a]
   (but the form of the posted constraint is different) 
"""
