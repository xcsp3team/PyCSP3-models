"""
Lightweight industrial robots such as YuMi by ABB Ltd. are designed to take over repetitive and tedious tasks from humans,
occupying similar floor area and having similar reach.
YuMi in particular caters to small-parts assembly manufacturing.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021/2022/2023/204 Minizinc challenges.
MIT Licence (Copyright 2021 Johan Ludde Wessénassumed)

## Data Example
  p-04-GG-GG-3.4.json

## Model
  constraints: AllDifferent, AllEqual, Count, Cumulative, Element, Maximum, Minimum, Precedence, Table

## Execution
  python Yumi.py -data=<datafile.dzn> -parser=Yumi_ParserZ.py -variant=static
  python Yumi.py -data=<datafile.dzn> -parser=Yumi_ParserZ.py -variant=dynamic

## Links
  - https://new.abb.com/products/robotics/robots/collaborative-robots/yumi/dual-arm
  - https://link.springer.com/article/10.1007/s10601-023-09345-4
  - https://link.springer.com/chapter/10.1007/978-3-030-58942-4_33
  - https://github.com/LuddeWessen/assembly-robot-manager-minizinc
  - https://www.minizinc.org/challenge2021/results2021.html
  - https://www.minizinc.org/challenge2022/results2022.html
  - https://www.minizinc.org/challenge2023/results2023.html
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn21, mzn22, mzn23, mzn24
"""

from pycsp3 import *

tasks, task_orderings, agents, locations, nSuctionCups, zones = data
tray_tasks, camera_tasks, output_task, empty_gripper_tasks = tasks
gripper_ordering, suction_ordering, fixture_ordering = task_orderings
durations, times, fixtureWorkObstruction = agents
location_order, tray_locations, camera_locations, fixture_locations, airgun_locations, output_locations = locations

assert variant() in ("static", "dynamic") and variant("static") == (zones is None)

nLocations, nAgents, nActualTasks = len(times[0]), len(durations), len(durations[0])  # number of actual tasks, i.e. excluding dummy start & end tasks
assert nAgents == 2
nTasks = nActualTasks + 2 * nAgents  # all tasks, including dummy start & end tasks
nFixtures = len(fixture_ordering)

gripper_tasks, suction_tasks, fixture_tasks = [sorted(set(v for t in m for v in t)) for m in (gripper_ordering, suction_ordering, fixture_ordering)]
depot_tasks, beg_depot_tasks, end_depot_tasks = [nActualTasks + v for v in range(2 * nAgents)], [nActualTasks + v for v in range(nAgents)], [
    nActualTasks + nAgents + v for v in range(nAgents)]

min_duration, max_duration = 1, max(max(row) for row in durations)
min_travel_time, max_travel_time, min_waittime = 1, max(v for agent_times in times for row in agent_times for v in row), 1


def location_domain(task):
    if task in tray_tasks:
        return tray_locations
    if task in camera_tasks:
        return camera_locations
    if task == output_task:
        return output_locations
    return list(range(nLocations))


def time_of(a, f1, f2):
    return sum(durations[a][i] + f1(times[a][l1][l2] for l1 in location_domain(i) for l2 in range(nLocations))
               for i in range(nActualTasks) if f2(times[a][l][l] for l in location_domain(i)) > -1)


time_budget = max(time_of(a, max, max) for a in range(nAgents))
min_time_budget = min(time_of(a, min, min) for a in range(nAgents))
minimax_time_budget = min(time_of(a, min, max) for a in range(nAgents))

delta_g = cp_array([1 if t in gripper_ordering[:, 0] else -1 if t in gripper_ordering[:, 1] else 0 for t in range(nTasks)])
delta_s = [] if len(suction_ordering) == 0 else cp_array(
    [1 if t in suction_ordering[:, 0] else -1 if t in suction_ordering[:, 2] else 0 for t in range(nTasks)])


def T1(t):
    return [(a, l) for a in range(nAgents) for l in location_domain(t) if times[a][l][l] >= 0]


def T2(t):
    return [
        (a, l1, l2, min_travel_time if l1 == l2 else times[a][l1][l2])
        for a in range(nAgents) for l1 in location_domain(t) if times[a][l1][l1] >= 0 for l2 in range(nLocations) if times[a][l2][l2] >= 0
    ]


agent = VarArray(size=nTasks, dom=range(nAgents))  # Which agent performs the task

# Route encodings - each of these encode the same information, but in different ways
succ = VarArray(size=nTasks, dom=range(nTasks))  # Task sequence encoding where successor[i] = j means task j follows task i
task = VarArray(size=nTasks, dom=range(nTasks))  # Task sequence encoding where task[i] = j means task j is i:th to be performed

# Time variables:
arrival_time = VarArray(size=nTasks, dom=range(time_budget + 1))  # when agent arrives at task
start_time = VarArray(size=nTasks, dom=range(time_budget + 1))  # when agent start working on task
end_time = VarArray(size=nTasks, dom=range(time_budget + 1))  # when agent finish working on task
next_arrival_time = VarArray(size=nTasks, dom=range(time_budget + 1))  # when agent arrives at next task

# waiting_time[i] is the time between the arrival time and the start time for the ith task
waiting_time = VarArray(size=nTasks, dom=range(min_waittime, time_budget + 1))

duration = VarArray(size=nTasks, dom=range(min_duration, max_duration + 1))  # duration of task
travel_time = VarArray(size=nTasks, dom=range(min_travel_time, max_travel_time + 1))  # travel time of going from task i to successor[i]

# Locations - locations are variable
location = VarArray(size=nTasks, dom=range(nLocations))
next_location = VarArray(size=nTasks, dom=range(nLocations))  # Used to induce traveltime between tasks

agent1_count = Var(dom=range(nTasks))  # tasks assigned to left arm

# cycle overlap is the time between the finish time of one arm and the finish time of the other arm
cycle_overlap = Var(dom=range(time_budget + 1))

period = Var(dom=range(minimax_time_budget // 2, time_budget + 1))
makespan = Var(dom=range(minimax_time_budget // 2, time_budget + 1))

load_g = VarArray(size=nTasks, dom={0, 1})

load_s = VarArray(size=nTasks, dom=range(nSuctionCups + 1))

satisfy(
    agent1_count == Count(agent, value=0),

    # encoding A
    [
        succ[end_depot_tasks[1]] == beg_depot_tasks[0],
        succ[end_depot_tasks[0]] == beg_depot_tasks[1]
    ],

    # encoding B
    [
        task[-1] == end_depot_tasks[1],
        task[0] == beg_depot_tasks[0],
        task[agent1_count - 1] == end_depot_tasks[0],
        task[agent1_count] == beg_depot_tasks[1]
    ],

    # fixing dummy tasks to correct agent
    [
        (
            agent[beg_depot_tasks[a]] == a,
            agent[end_depot_tasks[a]] == a
        ) for a in range(nAgents)
    ],

    # Constraint 1, row 5-6:
    [
        (
            location[end_depot_tasks[a]] == location[beg_depot_tasks[a]],
            location[end_depot_tasks[a]] == next_location[end_depot_tasks[a]],
            location[beg_depot_tasks[a]] == next_location[beg_depot_tasks[a]],
            next_location[beg_depot_tasks[a]] == location[succ[beg_depot_tasks[a]]]
        ) for a in range(nAgents)
    ],

    # overlapping cycles
    [next_arrival_time[t] == arrival_time[succ[t]] for t in beg_depot_tasks],

    # at least one agent starts at time 0
    [
        Minimum(next_arrival_time[beg_depot_tasks]) == 0,
        Maximum(next_arrival_time[beg_depot_tasks]) == cycle_overlap
    ],

    [
        (
            travel_time[t] == min_travel_time,
            duration[t] == min_duration,
            waiting_time[t] == min_waittime,
            start_time[t] == arrival_time[t],
            start_time[t] == end_time[t],
            start_time[t] == next_arrival_time[t]
        ) for t in depot_tasks
    ],

    # imposing circuits
    Circuit(succ, no_self_looping=True),

    # connecting successor Encoding (A) with "task" Encoding (B)
    [task[t + 1] == succ[task[t]] for t in range(nTasks - 1)],

    # tag(redundant)
    AllDifferent(task),

    # imposing valid tours
    [
        [agent[t] == agent[succ[t]] for t in range(nActualTasks)],
        [agent[t] == agent[succ[t]] for t in beg_depot_tasks],
        [agent[t] != agent[succ[t]] for t in end_depot_tasks]
    ],

    # imposing some locations
    [
        [location[t] in tray_locations for t in tray_tasks],
        [location[t] in camera_locations for t in camera_tasks],
        [location[t] in fixture_locations for t in fixture_tasks],
        location[output_task] in output_locations
    ],

    [next_location[t] == location[succ[t]] for t in range(nActualTasks)],

    # all tasks of a fixture must be done at the same location
    [AllEqual(location[t]) for t in fixture_ordering],

    # all tasks of different fixtures must be done at different locations
    AllDifferent(location[t[0]] for t in fixture_ordering),

    # some locations are only reachable by some agents tag(redundant)
    [(agent[t], location[t]) in T1(t) for t in range(nTasks)],

    #  computing travel times (depends on arm, location, next_location)
    [(agent[t], location[t], next_location[t], travel_time[t]) in T2(t) for t in range(nActualTasks)],

    #  ensuring core time constraints
    [
        [start_time[t] + duration[t] == end_time[t] for t in range(nActualTasks)],
        [end_time[t] + travel_time[t] == next_arrival_time[t] for t in range(nActualTasks)],
        [next_arrival_time[t] == arrival_time[succ[t]] for t in range(nActualTasks)],
        [arrival_time[t] + waiting_time[t] == start_time[t] for t in range(nActualTasks)],
        [(agent[t], duration[t]) in [(0, durations[0, t]), (1, durations[1, t])] for t in range(nActualTasks)]
    ],

    # first fixture tasks start immediately
    [start_time[t[0]] == arrival_time[t[0]] + min_waittime for t in fixture_ordering],

    # other fixture tasks start directly, or as soon as previous tasks finish
    [start_time[t[i + 1]] == max(arrival_time[t[i + 1]] + min_waittime, end_time[t[i]]) for t in fixture_ordering for i in range(len(t) - 1)],

    # non-fixture tasks starts when arriving at location
    [
        (
            start_time[t] == arrival_time[t] + min_waittime,
            waiting_time[t] == min_waittime
        ) for t in range(nActualTasks) if t not in fixture_tasks
    ],

    # respecting order imposed by suction and gripper pick-n-place
    [
        [next_arrival_time[t[i]] <= arrival_time[t[i + 1]] for t in suction_ordering for i in range(len(t) - 1)],
        [next_arrival_time[t[i]] <= arrival_time[t[i + 1]] for t in gripper_ordering for i in range(len(t) - 1)]
    ],

    # pick-n-place on the same arm (agent)
    [
        [AllEqual(agent[t]) for t in suction_ordering],
        [AllEqual(agent[t]) for t in gripper_ordering]
    ],

    # increasing arrival times
    [
        [Increasing(arrival_time[t]) for t in suction_ordering],
        [Increasing(arrival_time[t]) for t in gripper_ordering]
    ],

    # all component trays need to be at different locations
    AllDifferent(location[tray_tasks]),

    # making sure fixture is emptied before next assembly
    [end_time[t[-1]] <= start_time[t[0]] + period for t in fixture_ordering],

    # making sure no overlap of assembly tasks within an agent
    [start_time[beg_depot_tasks[a]] + period == start_time[end_depot_tasks[a]] for a in range(nAgents)],

    # computing the objective
    [
        [next_arrival_time[t] >= min_time_budget // 2 for t in end_depot_tasks],
        period == min(next_arrival_time[end_depot_tasks]),
        makespan == Maximum(next_arrival_time),
        cycle_overlap == max(start_time[beg_depot_tasks]),
        makespan == period + cycle_overlap,
    ],

    # enforcing sequencing of suction PnP tasks
    [Precedence(task, values=t) for t in suction_ordering],

    # enforcing sequencing of gripper PnP tasks
    [Precedence(task, values=t) for t in gripper_ordering],

    # gripper capacity constraints
    [
        [load_g[j] == (0 if j == 0 else load_g[j - 1] + delta_g[task[j]]) for j in range(nTasks)],
        [(task[j], load_g[j]) in [(v, 0) for v in empty_gripper_tasks] + [(w, ANY) for w in range(nTasks) if w not in empty_gripper_tasks] for j in
         range(1, nTasks)]
    ],

    # suction capacity constraints
    [load_s[j] == (0 if j == 0 else load_s[j - 1] + delta_s[task[j]]) for j in range(nTasks)] if delta_s else None,

    # tag(redundant) -- improves propagation
    If(
        agent[output_task] == 0,
        Then=[
            succ[output_task] == end_depot_tasks[0],
            succ[beg_depot_tasks[1]] in tray_tasks
        ],
        Else=[
            succ[output_task] == end_depot_tasks[1],
            succ[beg_depot_tasks[0]] in tray_tasks
        ]
    )
)

if zones is None:  # yumi-static
    left_max = Var(dom=range(max(location_order) + 1))


    def T3(p):
        assert p not in fixture_tasks
        return ([(0, l1, o2) for l1 in location_domain(p) if times[0][l1][l1] >= 0 and (o1 := location_order[l1]) <= fixtureWorkObstruction[0]
                 for l2 in range(nLocations) if o1 <= (o2 := location_order[l2])] +
                [(1, l1, o2) for l1 in location_domain(p) if times[1][l1][l1] >= 0 and ((o1 := location_order[l1]) >= fixtureWorkObstruction[1] or o1 < 0)
                 for l2 in range(nLocations) if o1 > (o2 := location_order[l2])])


    satisfy(
        [(agent[p], location[p], left_max) in T3(p) for p in range(nActualTasks) if p not in fixture_tasks]
    )

else:  # yumi-dynamic
    wait, work, travel = zones
    max_zones = max(v for m2 in (wait, work) for m in m2 for row in m for v in row)
    nZones = max_zones + 1

    work_blocker = VarArray(size=[nActualTasks, nZones], dom={0, 1})
    wait_blocker = VarArray(size=[nActualTasks, nZones], dom={0, 1})
    travel_blocker = VarArray(size=[nActualTasks, nZones], dom={0, 1})


    def T4(t, z, tab):
        return [(a, l1, 1 if z in tab[a][l1] else 0) for a in range(nAgents) for l1 in location_domain(t) if times[a][l1][l1] >= 0]


    def T5(t, z):
        return [(a, l1, l2, 1 if z in travel[a][l1][l2] else 0) for a in range(nAgents) for l1 in location_domain(t) if times[a][l1][l1] >= 0 for l2 in
                range(nLocations) if times[a][l2][l2] >= 0]


    TO = arrival_time[:nActualTasks] + start_time[:nActualTasks] + end_time[:nActualTasks]
    LO = waiting_time[:nActualTasks] + duration[:nActualTasks] + travel_time[:nActualTasks]

    satisfy(
        [(agent[t], location[t], work_blocker[t, z]) in T4(t, z, work) for t in range(nActualTasks) for z in range(nZones)],

        [(agent[t], location[t], wait_blocker[t, z]) in T4(t, z, wait) for t in range(nActualTasks) for z in range(nZones)],

        [(agent[t], location[t], next_location[t], travel_blocker[t, z]) in T5(t, z) for t in range(nActualTasks) for z in range(nZones)],

        [
            Cumulative(
                origins=TO + [w + period for w in TO],
                lengths=LO + LO,
                heights=WO + WO
            ) <= 1 for z in range(nZones) if (WO := wait_blocker[:, z] + work_blocker[:, z] + travel_blocker[:, z])
        ]
    )

minimize(
    period
)

""" Comments
One redundant constraint not coded for the moment: (about enforinge sequencing of fixture tasks)
"""

#     fixture_zones = [v for v in range(max_zones - len(fixture_locations) + 1, max_zones + 1)]  # by design the fixture zones are last
