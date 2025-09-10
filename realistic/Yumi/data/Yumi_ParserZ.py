from pycsp3.problems.data.parsing import *

nAgents = 2


def values(l):
    ns = numbers_in(l)
    return list(range(ns[0], ns[1] + 1)) if ".." in l else numbers_in(l)


skip_empty_lines(or_prefixed_by="%")
durations = [numbers_in(line())] + [numbers_in(next_line()) for _ in range(nAgents - 1)]
next_line(repeat=1)
skip_empty_lines(or_prefixed_by="%")
tray_tasks = decrement(values(line()))
camera_tasks = decrement(values(next_line()))
output_tasks = decrement(values(next_line()))
assert len(output_tasks) == 1
output_task = output_tasks[0]
next_line()
skip_empty_lines(or_prefixed_by="%")
empty_gripper_task = decrement(values(line()))

data['taks'] = OrderedDict(
    [("tray_tasks", tray_tasks), ("camera_tasks", camera_tasks), ('output_task', output_task), ('empty_gripper_task', empty_gripper_task)]
)

next_line()
skip_empty_lines(or_prefixed_by="%")
grippers = decrement([v for v in numbers_in(l) if v != -1] for l in next_lines(prefix_stop="|]"))
next_line()
skip_empty_lines(or_prefixed_by="%")
suctions = decrement([v for v in t if v != -1] for l in next_lines(prefix_stop="|]") if (t := numbers_in(l)))
next_line()
skip_empty_lines(or_prefixed_by="%")
fixtures = decrement([v for v in numbers_in(l) if v != -1] for l in next_lines(prefix_stop="|]"))

data['task_orderings'] = OrderedDict([("gripper", grippers), ("suction", suctions), ("fixture", fixtures)])

next_line()
skip_empty_lines(or_prefixed_by="%")
nSuctionCups = number_in(line())
next_line(repeat=1)

left_times = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
next_line(repeat=1)
right_times = [numbers_in(l) for l in next_lines(prefix_stop="|]")]
assert len(left_times) == len(right_times)
next_line()
skip_empty_lines(or_prefixed_by="%")
location_order = numbers_in(line())

fixtureWorkObstruction = numbers_in(next_line())
assert len(fixtureWorkObstruction) == nAgents
data['agents'] = OrderedDict([("task_durations", durations), ("times", [left_times, right_times]), ("fixtureWorkObstruction", fixtureWorkObstruction)])

tray_locations = decrement(values(next_line()))
camera_locations = decrement(values(next_line()))
fixture_locations = decrement(values(next_line()))
airgun_locations = decrement(values(next_line()))
output_locations = decrement(values(next_line()))

nLocations = len(location_order)
assert nLocations == len(left_times) == len(left_times[0]) == len(right_times) == len(right_times[0]) == len(
    tray_locations + camera_locations + fixture_locations + airgun_locations + output_locations)

data['locations'] = OrderedDict([("order", location_order), ('tray_locations', tray_locations),
                                 ('camera_locations', camera_locations), ('fixture_locations', fixture_locations), ('airgun_locations', airgun_locations),
                                 ('output_locations', output_locations)])

data['nSuctionCups'] = nSuctionCups

next_line()
skip_empty_lines(or_prefixed_by="%")

if line() is None:
    data['zones'] = None
else:  # yumy-dynamic

    def read_series(sets=False):
        t = []
        while not next_line()[-1] == ';':
            t.append(numbers_in(line()) if sets is False else read_sets(line()))
        return t


    def read_sets(l):
        l = l.replace(" ", "")
        return [numbers_in(tok) for tok in l[l.index('{') + 1:l.rindex('}')].split('},{')]


    wait_left = read_sets(line())
    wait_right = read_sets(next_line())
    work_left = read_sets(next_line())
    work_right = read_sets(next_line())
    next_line()
    travel_left = read_series(True)
    next_line()
    travel_right = read_series(True)
    assert nLocations == len(wait_left) == len(wait_right) == len(work_left) == len(work_right) == len(travel_left) == len(travel_left[0]) == len(
        travel_right) == len(travel_right[0])
    data['zones'] = OrderedDict([("wait", [wait_left, wait_right]), ("work", [work_left, work_right]), ("travel", [travel_left, travel_right])])
