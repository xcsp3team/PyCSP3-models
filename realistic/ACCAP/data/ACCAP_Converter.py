import json

from pycsp3.problems.data.parsing import *

# Illustrating how to convert from a JSON format to another one.
# Example: python3 ACCAP.py -data=a03-f20-t10.json -parser=ACCAP_Converter.py

name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

opDur = d.get("opDur")
cNum = d.get("cNum")
xCoor = d.get("xCoor")
assert len(opDur) == len(cNum) == len(xCoor)
data['flights'] = [OrderedDict([("duration", opDur[i]), ("counters", cNum[i]), ("starting", xCoor[i])]) for i in range(len(opDur))]
data['airlines'] = [decrement(t.get("set")) for t in d.get("FA")]
nAirlines = d.get("airlines")
nFlights = d.get("flights")
assert nAirlines == len(data['airlines']) and nFlights == len(data['flights'])
times = d.get("times")  # not used
