"""
Example: python3 Blackhole.py  -parser=Blackhole_Random.py 13 3 0
"""

import random
from math import ceil
from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

nEmployees = ask_number("Number of employees (e.g., 30)")
seed = ask_number("Seed")

a1, b1 = ceil(nEmployees / 100 * 60), ceil(nEmployees / 100 * 80)
a2, b2 = ceil(nEmployees / 100 * 30), ceil(nEmployees / 100 * 60)

random.seed(seed)

t = [[random.randrange(a1, b1) // 3 for _ in range(3)] for _ in range(5)] + [[random.randrange(a2, b2) // 3 for _ in range(3)] for _ in range(2)]

data["nEmployees"] = nEmployees
data["requirements"] = t

Compilation.string_data = "-" + "-".join(str(v) for v in ("{:03d}".format(nEmployees), "{:02d}".format(seed)))
