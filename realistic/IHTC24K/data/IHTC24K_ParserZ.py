from pycsp3.problems.data.parsing import *
from pycsp3.problems.data.parsing import split_with_rows_of_size, split_with_structure

nOccupants = number_in(line())
nPatients = number_in(next_line())
horizon = number_in(next_line())
nRooms = number_in(next_line())
oc_length_of_stay = numbers_in(next_line())
oc_gender = decrement(numbers_in(next_line()))
oc_room = decrement(numbers_in(next_line()))
data['occupants'] = OrderedDict([("length_of_stay", oc_length_of_stay), ("gender", oc_gender), ("room", oc_room)])
assert nOccupants == len(oc_length_of_stay) == len(oc_gender) == len(oc_room)

length_of_stay = numbers_in(next_line())
gender = decrement(numbers_in(next_line()))

max_incompatible = number_in(next_line())
incompatible_rooms = split_with_rows_of_size(numbers_in(next_line()), max_incompatible)
incompatible_rooms = decrement([[v for v in t if v > 0] for t in incompatible_rooms])

ln = next_line()
mandatory = [0 if tok == "false" else 1 for tok in ln[ln.index('[') + 1:ln.rindex(']')].split(", ")]
surgery_duration = numbers_in(next_line())
surgeon = decrement(numbers_in(next_line()))
nSurgeons = number_in(next_line())
ln = next_line()
max_surgery = split_with_rows_of_size(numbers_in(ln[ln.index('[') + 1:]), horizon)
release_day = numbers_in(next_line())
due_day = numbers_in(next_line())

data['patients'] = OrderedDict(
    [("length_of_stay", length_of_stay), ("gender", gender), ("incompatible_rooms", incompatible_rooms), ("mandatory", mandatory),
     ("surgery_duration", surgery_duration), ("surgeon", surgeon), ("release_day", release_day), ("due_day", due_day)])
assert all(nPatients == len(t) for t in [length_of_stay, gender, incompatible_rooms, mandatory, surgery_duration, surgeon, release_day, due_day])

data['max_surgery'] = max_surgery

data['room_capacities'] = numbers_in(next_line())
nTheaters = number_in(next_line())
ln = next_line()
data['max_ot'] = split_with_rows_of_size(numbers_in(ln[ln.index('[') + 1:]), horizon)
data['weight_selection'] = number_in(next_line())
data['weight_delay'] = number_in(next_line())
