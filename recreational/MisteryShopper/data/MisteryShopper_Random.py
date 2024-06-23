"""
Example: python3 MisteryShopper.py  -parser=MisteryShopper_Random.py 8 12 0 6 0
"""

import random

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

g = ask_number("Number of groups (e.g., 5)")
n = ask_number("Size of the groups (e.g., 12)")
kr = ask_number("Cumulated number of holes in visitor groups (e.g., 3")
ke = ask_number("Cumulated number of holes in visitee groups (e.g., 5")
seed = ask_number("Seed")

random.seed(seed)
tr = [n for _ in range(g)]
for _ in range(kr):
    tr[random.randrange(g)] -= 1

te = [n for _ in range(g)]
for _ in range(ke):
    te[random.randrange(g)] -= 1

data["visitorGroups"] = tr  # [n for _ in range(g)]
data["visiteeGroups"] = te

Compilation.string_data = "-" + "-".join(str(v) for v in (g, "{:02d}".format(n), kr, ke, seed))  # "{:02d}".format(seed)))
