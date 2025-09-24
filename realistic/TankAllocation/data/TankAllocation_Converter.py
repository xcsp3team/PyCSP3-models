import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# For example python AircraftAssemblyLine.py -data=test.json -parser=AircraftAssemblyLine_Converter.py [-export]


name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

print(d)
pb = d.get("problem")
cargos = pb.get("cargos")
assert int(cargos.get("@nb")) == len(cargos.get("cargo"))
for i, obj in enumerate(cargos.get("cargo")):
    assert int(obj.get("@id")) == i + 1 and obj.get("@name") == "c" + str(i + 1)
data['volumes'] = [int(obj.get("@volume")) for obj in cargos.get("cargo")]
cnfs = pb.get("incompatibles")
if cnfs is None:
    cnfs = []
elif not isinstance(cnfs.get("incompatible"), list):
    cnfs = [cnfs.get("incompatible")]
else:
    cnfs = cnfs.get("incompatible")
data['conflicts'] = decrement([[int(obj.get("@cargo1")), int(obj.get("@cargo2"))] for obj in cnfs])

tanks = pb.get("tanks")
nTanks = int(tanks.get("@nb"))
assert nTanks == len(tanks.get("tank"))
for i, obj in enumerate(tanks.get("tank")):
    assert int(obj.get("@id")) == i + 1
caps = [int(obj.get("@capa")) for obj in tanks.get("tank")]
imps = [obj.get("impossiblecargos") for obj in tanks.get("tank")]
imps = decrement([[int(v.get("@id")) for v in t] for imp in imps if
                  (t := [] if imp is None else [imp.get("cargo")] if isinstance(imp.get("cargo"), dict) else imp.get("cargo"),)])
nghs = [obj.get("neighbours") for obj in tanks.get("tank")]
nghs = decrement([[int(v.get("@id")) for v in t] for ngh in nghs if
                  (t := [] if ngh is None else [ngh.get("tank")] if isinstance(ngh.get("tank"), dict) else ngh.get("tank"),)])
data["tanks"] = [OrderedDict([("capacity", caps[i]), ("impossibleCargos", imps[i]), ("neighbors", nghs[i])]) for i in range(nTanks)]
