import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# For example python CarpetCutting.py -data=test.json -parser=CarpetCutting_Converter.py [-export]


name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

data['roll_wid'] = d.get("roll_wid")
data['max_roll_len'] = d.get("max_roll_len")

nRm = d.get("n_rm")

rm_rec_ids = decrement([obj.get("set") for obj in d.get("rm_rec_ids")])
rm_ori = decrement([obj.get("set") for obj in d.get("rm_ori")])
rm_max_len = d.get("rm_max_len")
rm_max_wid = d.get("rm_max_wid")
assert nRm == len(rm_rec_ids) == len(rm_ori) == len(rm_max_len) == len(rm_max_wid)
data['roomCarpets'] = [
    OrderedDict([("rectangleIds", rm_rec_ids[i]), ("possibleRotations", rm_ori[i]), ("maxLength", rm_max_len[i]), ("mawWidth", rm_max_wid[i])]) for i in
    range(nRm)]

nRc = d.get("n_rm_rec")
rm_rec_len, rm_rec_wid = d.get("rm_rec_len"), d.get("rm_rec_wid")
rm_rec_os_x, rm_rec_os_y = d.get("rm_rec_os_x"), d.get("rm_rec_os_y")
assert nRc == len(rm_rec_len) == len(rm_rec_wid) == len(rm_rec_os_x) == len(rm_rec_os_y)
data['rectangles'] = [
    OrderedDict([("length", rm_rec_len[i]), ("width", rm_rec_wid[i]), ("xOffsets", rm_rec_os_x[i]), ("yOffsets", rm_rec_os_y[i])])
    for i in range(nRc)]

nSt, st_len, st_wid = d.get("n_st"), d.get("st_len"), d.get("st_wid")
st_no_steps, st_min_steps, st_max_breaks = d.get("st_no_steps"), d.get("st_min_steps"), d.get("st_min_steps")
assert nSt == len(st_len) == len(st_wid) == len(st_no_steps) == len(st_min_steps) == len(st_max_breaks)
data['stairCarpets'] = [
    OrderedDict([("length", st_len[i]), ("width", st_wid[i]), ("nCoveredSteps", st_no_steps[i]), ("minSteps", st_min_steps[i]), ("maxCuts", st_max_breaks[i])])
    for i in range(nSt)]

pos = name.rfind("/")
Compilation.string_data = "-" + name[pos + 1:] if pos != -1 else name
