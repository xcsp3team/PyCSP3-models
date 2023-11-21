"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020/2022 Minizinc challenges.
The MZN model was proposed by Greame Gange, with a Licence that seems to be like the MIT Licence.

## Data Example
  070-070-15-070-04.json

## Model
  constraints: MaximumArg, Sum

## Execution
  python Tower.py -data=<datafile.json>
  python Tower.py -data=<datafile.dzn> -parser=Tower_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  real, mzn20, mzn22
"""

from pycsp3 import *

min_signal_strength, distances, demands, capacities = data
nHandsets, nTowers = len(demands), len(capacities)
maxPower, PowerScale = 10, 10000

rnk = TypeRank.ANY if variant("any") else TypeRank.FIRST

effective_power = cp_array([0] + [2 * (p - 1) * (p - 1) for p in range(1, maxPower + 1)])  # we add 0 for the constraint Element
attenuation = [[PowerScale / (distances[h][t] * distances[h][t]) for t in range(nTowers)] for h in range(nHandsets)]
attenuation_i = cp_array([[round(attenuation[h][t]) for t in range(nTowers)] for h in range(nHandsets)])


def min_transmit_power(t, h):
    return next((p for p in range(1, maxPower) if effective_power[p] * attenuation[h][t] >= min_signal_strength), maxPower + 1)


# pr[i] is the power of the ith tower
pr = VarArray(size=nTowers, dom=range(1, maxPower + 1))

# tr[j] is the tower of the jth handset
tr = VarArray(size=nHandsets, dom=range(nTowers))

# od[i] is 1 if the ith tower is overloaded
od = VarArray(size=nTowers, dom={0, 1})

# quality[j] is 1 if the tower of the jth handset is not overloaded
quality = VarArray(size=nHandsets, dom={0, 1})

satisfy(
    # choosing the right towers for handsets
    [tr[h] == MaximumArg([attenuation_i[h][t] * effective_power[pr[t]] for t in range(nTowers)], rank=rnk) for h in range(nHandsets)],

    # ensuring minimum signal strength
    [If(tr[h] == t, Then=pr[t] >= min_transmit_power(t, h)) for h in range(nHandsets) for t in range(nTowers)],

    # determining which towers are overloaded
    [od[t] == (Sum(demands[h] * (tr[h] == t) for h in range(nHandsets)) > capacities[t]) for t in range(nTowers)],

    # determining the connection quality of handsets
    [quality[h] != od[tr[h]] for h in range(nHandsets)]
)

maximize(
    # maximizing the connection quality of handsets
    Sum(quality)
)

"""
1) For the moment, we cannot write:
    [[pr[t] >= min_transmit_power(t, h) for t in range(nTowers)][tr[h]] == 1 for h in range(nHandsets)],
   It needs to redefine __get_item__ on list? is-it worthwhile?
   This is why another solution has been chosen 

2) valh Occs is very efficient

3) with rank=ANY, we got better solutions (because this is less constraining)
   For example, python Tower.py -data=tower_070_070_15_070-09.dzn -dataparser=Tower_ParserZ.py
   generates an instance where java ace Tower-tower_070_070_15_070-09.xml -valh=Occs has a greater bound than the MZN optimum
   
4) For the group 'minimum signal strength', two alternatives are:
  a)
    pt = VarArray(size=[nTowers, nHandsets], dom={0, 1})
    [pt[t, h] == (power[t] >= min_transmit_power(t, h)) for t in range(nTowers) for h in range(nHandsets)],
    [pt[:, h][tower[h]] == 1 for h in range(nHandsets)],
  
  b) 
    [attenuation_i[h, tower[h]] * effective_power[power[tower[h]]] >= min_signal_strength for h in range(nHandsets)],   
5) FIRST seems to be the semantics of MaximumArg in the MZN model 
"""
