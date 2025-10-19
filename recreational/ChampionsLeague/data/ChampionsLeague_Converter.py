import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

league_phase = d[:8 * 18]
data['schedule'] = [[(match['HomeTeam'], match['AwayTeam']) for j in range(18) if (match := league_phase[i * 18 + j])] for i in range(8)]

pos = name.rfind("/")
Compilation.string_data = "-" + name[pos + 1:] if pos != -1 else name
