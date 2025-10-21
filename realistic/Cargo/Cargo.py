"""
This is a real-world cargo assembly planning problem arising in a coal supply chain.
The cargoes are built on the stockyard at a port terminal from coal delivered by trains.
Then the cargoes are loaded onto vessels.
Only a limited number of arriving vessels is known in advance.
The goal is to minimize the average delay time of the vessels over a long planning period.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2017/2018 Minizinc challenges.
See links below to papers related to this problem.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  22.json

## Model
  constraints: Cumulative, Element, NoOverlap, Sum

## Execution
  python Cargo.py -data=<datafile.json>
  python Cargo.py -data=<datafile.dzn> -parser=Cargo_ParserZ.py

## Links
  - https://optimization-online.org/wp-content/uploads/2013/02/3755.pdf
  - https://www.sciencedirect.com/science/article/pii/S2192437620301217
  - https://link.springer.com/chapter/10.1007/978-3-319-07046-9_12
  - https://www.minizinc.org/challenge/2018/results/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  realistic, mzn13, mzn17, mzn18, xcsp24
"""

from pycsp3 import *

H, T, stackBefore, limits, coeffs, eta, piles = data or load_json_data("22.json")

vessels, r_sd, rd = zip(*piles)  # r_sd is for rounded stacking duration, rd is for (precise) reclaiming duration
nVessels, nPiles = len(eta), len(piles)

V, P = range(nVessels), range(nPiles)

vrd = [sum(rd[i] for i in P if vessels[i] == j) for j in V]  # reclaiming duration summed for vessels
dailyStackingTonnages = [(rd[i] * coeffs.tonnage) // (r_sd[i] * coeffs.time) for i in P]
lengths = [((rd[i] * coeffs.length) // coeffs.hour + coeffs.meter - 1) // coeffs.meter for i in P]
lastPiles = [max(i for i in P if vessels[i] == j) for j in V]  # for each vessel

# r_st[i] is the rounded stacking start time of the ith stockpile
r_st = VarArray(size=nPiles, dom=range(T // coeffs.time + 1))

# st[i] is the precise stacking start time of the ith stockpile
st = VarArray(size=nPiles, dom=range(T + 1))

# y[i] is the rounded position of the ith stockpile
y = VarArray(size=nPiles, dom=range(H // coeffs.meter + 1))

# rt[i] is the reclaiming start time of the ith stockpile
rt = VarArray(size=nPiles, dom=range(T + 1))

# r_dt[i] is the rounded total duration time of processing the ith stockpile
r_dt = VarArray(size=nPiles, dom=range(T // coeffs.time + 1))

# dt[i] is the precise total duration time of processing the ith stockpile
dt = VarArray(size=nPiles, dom=range(T + 1))

# ft[i] is the finishing time, when the ith vessel is ready to leave
ft = VarArray(size=nVessels, dom=range(T + 1))

# y2 = VarArray(size=nPiles, dom=lambda i: {lengths[i]})  # introduced for respecting the perimeter of the 2024 competition


satisfy(
    # linking precise and rounded stacking start times
    [st[i] == r_st[i] * coeffs.time for i in P],

    # linking precise and rounded total processing times
    [dt[i] == r_dt[i] * coeffs.time for i in P],

    # making vessels ready when reclaiming is finished
    [ft[j] == rt[lastPiles[j]] + rd[lastPiles[j]] for j in V],

    # computing total processing times
    [dt[i] >= rt[i] + rd[i] - st[i] for i in P],

    # finishing in time
    [r_st[lastPiles[j]] + r_dt[lastPiles[j]] <= (T + coeffs.time - 1) // coeffs.time for j in V],

    # reclaiming of a stockpile cannot start before the ETA of its vessel
    [rt[i] >= eta[vessels[i]] for i in P],

    # stacking of a stockpile starts when possible
    [st[i] >= eta[vessels[i]] - stackBefore * coeffs.time for i in P],

    # respecting the continuous reclaim time limit (e.g., 5 hours)
    [rt[i + 1] <= rt[i] + rd[i] + limits.maxReclaimingGap for i in P[:-1] if vessels[i] == vessels[i + 1]],

    # stacking of a stockpile has to complete before reclaiming can start
    [r_st[i] + r_sd[i] <= rt[i] // coeffs.time for i in P],

    # ensuring stockpiles fit on their pads
    [y[i] + lengths[i] <= H // coeffs.meter for i in P],

    # respecting the reclaim order of the stockpiles of a vessel
    [rt[i] + rd[i] <= rt[i + 1] for i in P[:-1] if vessels[i] == vessels[i + 1]],

    # computing the sum of vessel delays
    Sum(ft[j] - eta[j] - vrd[j] for j in V) <= limits.sumMaxDelay,
    # sum_delay == Sum(ft[j] - eta[j] - vrd[j] for j in range(nVessels)),

    # not exceeding a maximum delay
    [ft[j] - eta[j] - vrd[j] <= limits.maxDelay for j in V],

    # not overlapping stockpiles in space and time
    NoOverlap(
        origins=(r_st, y),
        lengths=(r_dt, lengths)  # y2 used instead of lengths for the competition
    ),

    # not exceeding the pad lengths
    Cumulative(
        origins=r_st,
        lengths=r_dt,
        heights=lengths
    ) <= H // coeffs.meter,

    # not exceeding the daily stacking capacity
    Cumulative(
        origins=r_st,
        lengths=r_sd,
        heights=dailyStackingTonnages
    ) <= limits.dailyStacking,

    # ensuring that there are always enough reclaimers
    Cumulative(
        origins=rt,
        lengths=rd,
        heights=1
    ) <= limits.nReclaimers
)

minimize(
    Sum(ft[j] - eta[j] - vrd[j] for j in V[4:-5])
)

""" Comments
1) comb that seems to be used to guide search (in the MZn model) is not inserted above
 comb = flatten([[tR[i], tS__[i], h__[i]][k] for i in range(nPiles) for k in range(3)])
2) The following variable is not computed (because non necessary)
# sum_delay is the sum of vessel delays (waiting times)
# sum_delay = Var(range(limits.sumMaxDelay + 1))
"""

# [(r_st[i], rt[i]) in [(v, ge((v + r_sd[i]) * coeffs.time)) for v in r_st[i].dom] for i in P],
