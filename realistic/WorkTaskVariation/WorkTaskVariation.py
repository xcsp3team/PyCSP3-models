"""
Work Task Variation problem (WTV)

From CP'25 paper (cited below) Given a schedule with fixed worker time slots and task assignments, the core challenge of the WTV problem
lies in rearranging tasks between workers while preserving the original time slot allocations to improve flow and ergonomics.
The cost function penalizes both excessively short and long spans of a single task, aiming for a balanced variety minimizing repetitive strain
and promotes engagement.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
The original mzn model by Mikael Zayenz Lagerkvist and Magnus Rattfeldt -- No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  s03-l10-o08-w12-b15.json

## Model
  constraints: Cardinality, Element, Regular, Sum

## Execution
  python WorkTaskVariation.py -data=<datafile.json>
  python WorkTaskVariation.py -data=<datafile.dzn> -parser=WorkTaskVariation_ParserZ.py

## Links
  - https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2025.24
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
"""

from pycsp3 import *

fixed, requirements, activity_run_costs, activity_frequency_costs = data or load_json_data("s03-l10-o08-w12-b15.json")

nResources, nSlots = len(fixed), len(fixed[0])
nActivities = 5  # [T, S, W, o, b]
NONE = nActivities

extended_activity_run_costs = activity_run_costs + [[0] * (nSlots + 1)]

R, S, A = range(nResources), range(nSlots), range(nActivities)

Aut = Automaton(
    start=(q := Automaton.q)(0),
    final=[q(1), q(2), q(3)],
    transitions=[(q(0), NONE, q(1)), (q(1), NONE, q(1)), (q(0), ne(NONE), q(2)), (q(1), ne(NONE), q(2)), (q(2), ne(NONE), q(2)), (q(2), NONE, q(3)),
                 (q(3), NONE, q(3))]
)  # automaton for None* [^None]* None*

# schedule[r][s] is the activity for resource r in slot s
schedule = VarArray(size=[nResources, nSlots], dom=range(nActivities + 1))  # +1 for None

# run_end[r][s] is 1 if the slot s is the end of an activity for the resource r
run_end = VarArray(size=[nResources, nSlots], dom={0, 1})

# run_length[r][s] is the current length, at slot s, of the activity started for the resource r
run_length = VarArray(size=[nResources, nSlots], dom=range(nSlots + 1))

# run_cost[r][s] is the cost of the activity that ends in slot s for the resource r
run_cost = VarArray(size=[nResources, nSlots], dom=extended_activity_run_costs)

# frequency_cost[r][a] is the frequency cost of the number of runs of the activity a for the resource r
frequency_cost = VarArray(size=[nResources, nActivities], dom=activity_frequency_costs)

# frequency_cost[r][a] is the number of times the activity a has been run (and ended) for the resource r
frequency_ends = VarArray(size=[nResources, nActivities], dom=range(nSlots + 1))

satisfy(
    # ensuring all shifts are only Activities (i.e., not None) surrounded with None
    [
        Regular(
            scope=schedule[r],
            automaton=Aut
        ) for r in R
    ],

    # respecting requirements for each slot (column in the schedule)
    [
        Cardinality(
            within=schedule[:, s],
            occurrences={a: requirements[a][s] for a in A} | {NONE: nResources - sum(requirements[:, s])}
        ) for s in S
    ],

    # respecting fixed requirements
    [schedule[r][s] == fixed[r][s] for r in R for s in S if fixed[r][s] != -1],

    # managing runs
    [
        [run_end[r][s] == (1 if s == nSlots - 1 else (schedule[r][s] != schedule[r][s + 1])) for r in R for s in S],
        [run_length[r][s] == (1 if s == 0 else ift(run_end[r][s - 1], 1, run_length[r][s - 1] + 1)) for r in R for s in S],
        [run_cost[r][s] == ift(run_end[r][s], extended_activity_run_costs[schedule[r][s], run_length[r][s]], 0) for r in R for s in S]
    ],

    # managing frequency costs
    [
        [frequency_ends[r][a] == Sum(both(run_end[r][s], schedule[r][s] == a) for s in S) for r in R for a in A],
        [frequency_cost[r][a] == activity_frequency_costs[a, frequency_ends[r][a]] for r in R for a in A]
    ]
)

minimize(
    Sum(run_cost) + Sum(frequency_cost)
)
