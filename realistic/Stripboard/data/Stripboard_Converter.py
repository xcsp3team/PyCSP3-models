import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# For example python Stripboard.py -data=test.json -parser=Stripboard_Converter.py [-export]


name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

max_w = d.get("max_w")
max_h = d.get("max_h")
max_links = d.get("max_links")
tc = d.get("COMPONENT")
tp = d.get("PIN")
tn = d.get("NET")
footprint_w = d.get("footprint_w")
footprint_h = d.get("footprint_h")
allowed_orientation = d.get("allowed_orientation")
pin_dx = d.get("pin_dx")
pin_dy = d.get("pin_dy")
pin_net = d.get("pin_net")
pins_struct = d.get("pins")

nComponents, nPins = len(tc), len(pin_dx)

data['max_w'] = max_w
data['max_h'] = max_h
data['max_links'] = max_links
data['components'] = [(tc[i], footprint_w[i], footprint_h[i], allowed_orientation[i].get("set")) for i in range(nComponents)]

m = [pins_struct[i].get("set") for i in range(nComponents)]
pins = []
cnt = 0
for t in m:
    tt = []
    for name in t:
        tt.append((name, pin_dx[cnt], pin_dy[cnt], pin_net[cnt]))
        cnt += 1
    pins.append(tt)
data['pins'] = pins
data['nets'] = tn

pos = name.rfind("/")
Compilation.string_data = "-" + name[pos + 1:] if pos != -1 else name
