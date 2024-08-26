"""
We have n trains moving along a single track with m stations.
There is a non-zero constant flow of passengers arriving at all but the first and last station who wish to travel to the final station.
Trains are originally scheduled so that they collect the passengers and drop them at the final station.
To this original schedule a disruption is introduced whereby a train is delayed.
Each of the trains (at the time of the delay) has knowledge of the duration of the delay.
The objective is to reschedule the trains to minimize the average travel time of the passengers.
Trains are not able to overtake preceding trains, however they do have the option to skip a station and wait longer at a station to collect more passengers.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012/2014/2018 Minizinc challenges.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  01.json

## Model
  constraints: Sum

## Execution
  python Train.py -data=<datafile.json>
  python Train.py -data=<datafile.dzn> -parser=Train_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, mzn12, mzn14, mzn18
"""

from pycsp3 import *

maxTime, delay, stations, trains, capacity = data
passengerStarts, passengerFlows, distances = zip(*stations)
arrSchedules, depSchedules = zip(*trains)
nTrains, nStations = len(trains), len(stations)

horizon = maxTime + 1
delayStation = min(j for j in range(nStations) if depSchedules[delay.train][j] > delay.time)  # destination when delayed

# arr[i][j] is the time at which the ith train arrives at the jth station
arr = VarArray(size=[nTrains, nStations], dom=range(horizon))

# dep[i][j] is the time at which the ith train leaves (departs from) the jth station
dep = VarArray(size=[nTrains, nStations], dom=range(horizon))

# sigmaL[i][j] is the signal permitting to start boarding in the ith train at the jth station
sigmaL = VarArray(size=[nTrains, nStations], dom=range(horizon))

# sigmaU[i][j] is the signal forbidding to keep boarding in the ith train at the jth station
sigmaU = VarArray(size=[nTrains, nStations], dom=range(horizon))

# collect[i][j] is the number of passengers collected by the ith train at the jth station
collect = VarArray(size=[nTrains, nStations], dom=range(capacity + 1))

# load[i][j] is the load (number of passengers) of the ith train when leaving the jth station
load = VarArray(size=[nTrains, nStations], dom=range(capacity + 1))

# dwell[i][j] is the dwelling time of the ith train at the jth station
dwell = VarArray(size=[nTrains, nStations], dom=range(horizon))

satisfy(
    # all trains 'arrive' at the first station at time 0
    [arr[i][0] == 0 for i in range(nTrains)],

    # all trains 'depart' from the last station as soon as they arrive there
    [dep[i][-1] == arr[i][-1] for i in range(nTrains)],

    # handling the (fictive) delay
    [
        # before the delay, the schedule is respected
        [dep[i][j] == depSchedules[i][j] for i in range(nTrains) for j in range(nStations - 1) if depSchedules[i][j] <= delay.time],

        # if in motion, the arrival of the delayed train is at least the departure time at the previous station
        # plus the ordinary travel time plus the duration of the delay
        arr[i][j] >= dep[i][j - 1] + delay.duration + distances[j - 1]
        if (i := delay.train, j := delayStation) and j > 0 and delay.time < depSchedules[i][j - 1] + distances[j - 1] else None,

        # the train's next departure is at least the delay time plus the delay duration
        dep[delay.train][delayStation] >= delay.time + delay.duration
    ],

    # trains depart after they arrive
    [dep[i][j] >= arr[i][j] for i in range(nTrains) for j in range(nStations)],

    # trains never depart earlier than scheduled
    [dep[i][j] >= depSchedules[i][j] for i in range(nTrains) for j in range(nStations - 1)],

    # ensuring a minimum travel time between stations
    [arr[i][j + 1] >= dep[i][j] + distances[j] for i in range(nTrains) for j in range(nStations - 1)],

    # at first station, trains leave in order
    [dep[i][0] < dep[i + 1][0] for i in range(nTrains - 1)],

    # at most one train dwelling at a station at a given time
    [dep[i][j] <= arr[i + 1][j] - 2 for i in range(nTrains - 1) for j in range(1, nStations - 1)],

    # the sigma values partition time at each station
    [sigmaL[i][j] <= sigmaU[i][j] for i in range(nTrains) for j in range(nStations)],

    # for the first and last trains, the sigma values are equal to the extreme times of passenger arrivals
    [
        (
            sigmaL[0][j] == passengerStarts[j],
            sigmaU[-1][j] == depSchedules[-1][j]
        ) for j in range(1, nStations - 1)
    ],

    # the sigma values join together
    [sigmaU[i][j] == sigmaL[i + 1][j] for i in range(nTrains - 1) for j in range(nStations)],

    # you can't pick up people after you leave
    [
        [sigmaU[i][j] <= dep[i][j] for i in range(nTrains - 1) for j in range(nStations - 1)],
        [sigmaU[-1][j] <= dep[-1][j] for j in range(nStations - 1)],
    ],

    # managing collect and load variables
    [
        [collect[i][j] == (sigmaU[i][j] - sigmaL[i][j]) * passengerFlows[j] for i in range(nTrains) for j in range(nStations)],
        [load[i][0] == collect[i][0] for i in range(nTrains)],
        [load[i][j] == load[i][j - 1] + collect[i][j] for i in range(nTrains) for j in range(1, nStations)],
    ],

    # if a train picks anyone up, then it must pick everyone up
    [
        If(
            sigmaU[i][j] > sigmaL[i][j],
            Then=disjunction(
                sigmaU[i][j] == dep[i][j],
                sigmaU[i][j] == depSchedules[-1][j],
                load[i][j] + (sigmaU[i][j] < depSchedules[-1][j]) * passengerFlows[j] > capacity
            )
        ) for i in range(nTrains) for j in range(nStations - 1)
    ],

    # managing boarding time
    [
        If(
            capacity - load[i][j - 1] < 100,
            Then=collect[i][j] <= dwell[i][j] * 20,
            Else=collect[i][j] <= dwell[i][j] * 50
        ) for i in range(nTrains) for j in range(1, nStations)
    ],

    [collect[i][0] <= (dep[i][0] - arr[i][0]) * 50 for i in range(nTrains)],

    # tag(redundant)
    [collect[i][j] <= (dep[i][j] - arr[i][j]) * 50 for i in range(nTrains) for j in range(1, nStations)],

    # computing dwelling times of trains in stations
    [dwell[i][j] == dep[i][j] - arr[i][j] for i in range(nTrains) for j in range(nStations)]
)

minimize(
    # minimizing the number of transported people combined with the time take taken to transport them
    Sum(load[i][-1] * arr[i][-1] for i in range(nTrains))
)

"""
1) some other ways of posting constraints are:
  arr[delay.train][delayStation] >= dep[delay.train][delayStation - 1] + delay.duration + distances[delayStation - 1]
 if delayStation > 0 and delay.time < depSchedules[delay.train][delayStation - 1] + distances[delayStation - 1] else None,

 [(sigmaU[i][j] <= sigmaL[i][j]) | (sigmaU[i][j] == dep[i][j]) | (sigmaU[i][j] == depSchedules[-1][j]) |
  (load[i][j] + (sigmaU[i][j] < depSchedules[-1][j]) * passengerFlows[j] > capacity) for i in range(nTrains) for j in range(nStations - 1)],

 [(capacity - load[i][j - 1] >= 100) | (collect[i][j] <= dwell[i][j] * 20) for i in range(nTrains) for j in range(1, nStations)],
 [(capacity - load[i][j - 1] < 100) | (collect[i][j] <= dwell[i][j] * 50) for i in range(nTrains) for j in range(1, nStations)],
"""
