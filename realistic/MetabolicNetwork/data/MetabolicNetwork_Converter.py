import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# For example python MetabolicNetwork.py -data=test.json -parser=MetabolicNetwork_Converter.py [-export]


name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

reactions = d.get("reactions")
metabolites = d.get("metabolites")
smatrix = d.get("smatrix")
rmatrix = d.get("rmatrix")
assert len(reactions) == len(smatrix[0])
assert len(rmatrix) == 0 or len(reactions) == len(rmatrix[0])
assert len(metabolites) == len(smatrix)

data['nReactions'] = len(reactions)
data['stoichiometryMatrix'] = smatrix
data['reversibleIndicators'] = rmatrix

pos = name.rfind("/")
Compilation.string_data = "-" + name[pos + 1:] if pos != -1 else name
