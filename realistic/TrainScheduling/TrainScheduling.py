"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  05.json

## Model
  constraints: AllDifferent, Cumulative, Element, NoOverlap, Sum

## Execution
  python TrainScheduling.py -data=<datafile.json>
  python TrainScheduling.py -data=<datafile.dzn> -parser=TrainScheduling_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
"""

from pycsp3 import *

stops, routes, services, engines, makespan, min_sep = data

nStops, nRoutes, nServices, nEngines, nSteps = len(stops.types), len(routes), len(services.routes), len(engines.names), len(routes[0])  # max_route_length
S, I = range(nServices), range(nSteps)

TERMINUS, ORDINARY, HUB = range(3)
SING, DOUB, QUAD, NONE = range(4)
DUMMY = nStops - 1  # also dstop

sroutes = cp_array([routes[services.routes[s]] for s in S])
_rlength = [next((i for i in I if route[i] == DUMMY), nSteps) for route in routes]
slengths = cp_array([_rlength[services.routes[s]] for s in S])


def structures(stop1, stop2):
    service_left = [s for s in S if any(True for i in range(slengths[s] - 1) if sroutes[s][i] == stop1 and sroutes[s][i + 1] == stop2)]
    stop_left = [i for s in S for i in range(slengths[s] - 1) if sroutes[s][i] == stop1 and sroutes[s][i + 1] == stop2]
    service_right = [s for s in S if any(True for i in range(slengths[s] - 1) if sroutes[s][i] == stop2 and sroutes[s][i + 1] == stop1)]
    stop_right = [i for s in S for i in range(slengths[s] - 1) if sroutes[s][i] == stop2 and sroutes[s][i + 1] == stop1]
    return service_left, stop_left, service_right, stop_right


# arrive[s][i] is the arriving time at the ith step for service s
arrive = VarArray(size=[nServices, nSteps], dom=range(makespan + 1))

# depart[s][i] is the starting time at the ith step for service s
depart = VarArray(size=[nServices, nSteps], dom=range(makespan + 1))

# waiting[s][i] is the waiting time at the ith step for service s
waiting = VarArray(size=[nServices, nSteps], dom=range(makespan + 1))

# stopped[s][i] is 1 if there is a real stop at the ith step for service s
stopped = VarArray(size=[nServices, nSteps], dom={0, 1})

# eng[s] is the engine used for service s
eng = VarArray(size=nServices, dom=range(nEngines))

# prv[s] is the previous engine or service for service s
prv = VarArray(size=nServices, dom=range(nEngines + nServices))

satisfy(
    ### STAGE A - schedule constraints

    #  A service starts after its service start time
    [arrive[s][0] >= services.starts[s] for s in S],

    # the departure time is at least the minimal_wait time for the stop after arrival
    [waiting[s][i] == depart[s][i] - arrive[s][i] for s in S for i in I],

    [waiting[s][i] >= stopped[s][i] * stops.minimal_waits[sroutes[s][i]] for s in S for i in I],

    # the arrival time for the next stop is at least the travel time after the departure from previous stop
    [arrive[s][i + 1] >= depart[s][i] + stops.travel_times[sroutes[s][i]][sroutes[s][i + 1]] for s in S for i in range(slengths[s] - 1)],

    # for dummy stops, just copy the last depart time
    [
        (
            arrive[s][i + 1] == depart[s][i],
            depart[s][i + 1] == depart[s][i]
        ) for s in S for i in range(slengths[s] - 1, nSteps - 1)
    ],

    ### STAGE B - stop constraints

    [
        Cumulative(
            origins=arrive[T],  # equivalent to [arrive[s][i] for s, i in T]
            lengths=waiting[T],
            heights=1
        ) <= K
        for j, K in enumerate(stops.n_platforms) if j != DUMMY and nEngines > K and (T := [(s, i) for s in S for i in I if sroutes[s][i] == j])
    ],

    ### STAGE C - objective constraints

    [stopped[s][i] for s in S for i in I if stops.types[sroutes[s][i]] != ORDINARY],

    ### STAGE D -- engine assignment

    # if the previous assignment is an engine the start location of the service and engine must agree
    [
        If(
            prv[s] < nEngines,
            Then=[(aux := Var()) == prv[s], sroutes[s][0] == engines.starts[aux]]
        ) for s in S
    ],

    #  engine of the train is the given engine or engine of previous routs
    [
        If(
            prv[s] < nEngines,
            Then=eng[s] == prv[s],
            Else=[(aux := Var()) == prv[s] - nEngines, eng[s] == eng[aux]]
        ) for s in S
    ],

    # engine transfer from same location
    [
        If(
            prv[s] >= nEngines,
            Then=[(aux := Var()) == prv[s] - nEngines, sroutes[s][0] == sroutes[aux][slengths[aux] - 1]]
        ) for s in S
    ],

    # engine implies time precedence
    [
        If(
            prv[s] >= nEngines,
            Then=[(aux := Var()) == prv[s] - nEngines, arrive[s][0] >= depart[aux][slengths[aux] - 1]]
        ) for s in S
    ],

    AllDifferent(prv),
)

if nEngines > 1:
    for stop1, stop2 in combinations(nStops, 2):
        if stops.lines[stop1][stop2] == DOUB:
            srvl, stpl, srvr, stpr = structures(stop1, stop2)  # serviceleft, stopleft, serviceright, stopright
            nLeft, nRight = len(srvl), len(srvr)

            if nLeft > 1:
                satisfy(
                    NoOverlap(origins=[depart[srvl[i]][stpl[i]] for i in range(nLeft)], lengths=min_sep),

                    [(depart[srvl[i]][stpl[i]] < depart[srvl[j]][stpl[j]]) == (arrive[srvl[i]][stpl[i] + 1] + min_sep <= arrive[srvl[j]][stpl[j] + 1])
                     for i, j in combinations(nLeft, 2)]
                )

            if nRight > 1:
                satisfy(
                    NoOverlap(origins=[depart[srvr[i]][stpr[i]] for i in range(nRight)], lengths=min_sep),

                    [(depart[srvr[i]][stpr[i]] < depart[srvr[j]][stpr[j]]) == (arrive[srvr[i]][stpr[i] + 1] + min_sep <= arrive[srvr[j]][stpr[j] + 1])
                     for i, j in combinations(nRight, 2)]
                )

    for stop1, stop2 in combinations(nStops, 2):
        if stops.lines[stop1][stop2] == SING:
            srvl, stpl, srvr, stpr = structures(stop1, stop2)
            nLeft, nRight = len(srvl), len(srvr)
            allserv, allstop = cp_array(srvl + srvr), cp_array(stpl + stpr)
            nLocal = nLeft + nRight
            if nLocal > 1:
                _next = VarArray(size=nLocal + 1, dom=range(nLocal + 1), id="next_" + str(stop1) + "_" + str(stop2))  # nLocal is a special value

                satisfy(
                    AllDifferent(_next),

                    [
                        If(
                            _next[i] < nLeft,
                            Then=depart[allserv[_next[i]], allstop[_next[i]]] >= min_sep + depart[allserv[i], allstop[i]],
                            Else=If(
                                _next[i] != nLocal,
                                Then=depart[allserv[_next[i]], allstop[_next[i]]] >= arrive[allserv[i], allstop[i] + 1]
                            )
                        ) for i in range(nLeft)
                    ],

                    [
                        If(
                            _next[i] < nLeft,
                            Then=depart[allserv[_next[i]], allstop[_next[i]]] >= arrive[allserv[i], allstop[i] + 1],
                            Else=If(
                                _next[i] != nLocal,
                                Then=depart[allserv[_next[i]], allstop[_next[i]]] >= min_sep + depart[allserv[i], allstop[i]]
                            )
                        )
                        for i in range(nLeft, nLocal)
                    ]
                )

minimize(
    Sum(abs(depart[s][-1] - services.ends[s]) for s in S)
    + Sum(stops.skip_costs[sroutes[s][i]] * (1 - stopped[s][i]) for s in S for i in I)
)

""" Comments
1) Note the form of the statement:
   [(aux := Var()) == prv[s] - nEngines, eng[s] == eng[aux]]
  An auxiliary variable is defined to be used with a constraint Element.
  Its domain will be automatically set to the index range of the array 'eng'.
  If instead we write:
    [eng[s] == eng[prv[s] - nEngine]]
  we have an error (the domain of values of the expression prv[s] - nEngines being incompatible with the index range of the array 'eng' 
"""
