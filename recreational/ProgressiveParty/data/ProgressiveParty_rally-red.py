"""
Example: python progressiveParty.py  -parser=ProgressiveParty_rally-red.py 42 9
"""

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

nBoats = ask_number("Number of boats")
assert 3 <= nBoats <= 42
data["nPeriods"] = nPeriods = ask_number("Number of periods")

rally_red = [
    [6, 2],
    [8, 2],
    [12, 2],
    [12, 2],
    [12, 4],
    [12, 4],
    [12, 4],
    [10, 1],
    [10, 2],
    [10, 2],
    [10, 2],
    [10, 3],
    [8, 4],
    [8, 2],
    [8, 3],
    [12, 6],
    [8, 2],
    [8, 2],
    [8, 4],
    [8, 2],
    [8, 4],
    [8, 5],
    [7, 4],
    [7, 4],
    [7, 2],
    [7, 2],
    [7, 4],
    [7, 5],
    [6, 2],
    [6, 4],
    [6, 2],
    [6, 2],
    [6, 2],
    [6, 2],
    [6, 2],
    [6, 2],
    [6, 4],
    [6, 5],
    [9, 7],
    [0, 2],
    [0, 3],
    [0, 4]
]

data["boats"] = [OrderedDict([("capacity", ca), ("crewSize", cr)]) for (ca, cr) in rally_red[:nBoats]]

Compilation.string_data = "-" + "-".join(str(v) for v in ("{:02d}".format(nBoats), "{:02d}".format(nPeriods)))
