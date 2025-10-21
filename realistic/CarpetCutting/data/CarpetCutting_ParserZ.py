from pycsp3.problems.data.parsing import *

data['roll_width'] = number_in(line())
data['max_roll_length'] = number_in(next_line())
nRm = number_in(next_line())
l = next_line()
rm_rec_ids = decrement([numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("}, {")])
l = next_line()
rm_ori = decrement([numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("}, {")])
rm_max_len = numbers_in(next_line())
rm_max_wid = numbers_in(next_line())
assert nRm == len(rm_rec_ids) == len(rm_ori) == len(rm_max_len) == len(rm_max_wid)
data['roomCarpets'] = [
    OrderedDict([("rectangleIds", rm_rec_ids[i]), ("possibleRotations", rm_ori[i]), ("maxLength", rm_max_len[i]), ("mawWidth", rm_max_wid[i])])
    for i in range(nRm)]
nRc = number_in(next_line())
rm_rec_len = numbers_in(next_line())
rm_rec_wid = numbers_in(next_line())
next_line()
rm_rec_os_x = [numbers_in(next_line()) for _ in range(nRc)]
next_line(repeat=1)
rm_rec_os_y = [numbers_in(next_line()) for _ in range(nRc)]
assert nRc == len(rm_rec_len) == len(rm_rec_wid) == len(rm_rec_os_x) == len(rm_rec_os_y)
data['rectangles'] = [
    OrderedDict([("length", rm_rec_len[i]), ("width", rm_rec_wid[i]), ("xOffsets", rm_rec_os_x[i]), ("yOffsets", rm_rec_os_y[i])])
    for i in range(nRc)]
next_line()
nSt = number_in(next_line())
st_len = numbers_in(next_line())
st_wid = numbers_in(next_line())
st_no_steps = numbers_in(next_line())
st_min_steps = numbers_in(next_line())
st_max_breaks = numbers_in(next_line())
assert nSt == len(st_len) == len(st_wid) == len(st_no_steps) == len(st_min_steps) == len(st_max_breaks)
data['stairCarpets'] = [
    OrderedDict([("length", st_len[i]), ("width", st_wid[i]), ("nCoveredSteps", st_no_steps[i]), ("minSteps", st_min_steps[i]), ("maxCuts", st_max_breaks[i])])
    for i in range(nSt)]
