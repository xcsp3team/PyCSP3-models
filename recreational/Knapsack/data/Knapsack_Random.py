"""
Example: python3 Knapsack.py  -parser=Knapsack_Random.py 50 250 0
"""

import random

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

nObjects = ask_number("Number of objects (e.g., 50)")
capacity = ask_number("Capacity (e.g., 250)")
seed = ask_number("Seed")
MAX_PROFIT = 100  # hard coding

random.seed(seed)

weights = [random.randrange(1, capacity // 4) for _ in range(nObjects)]
values = [random.randrange(1, MAX_PROFIT) for _ in range(nObjects)]

data["capacity"] = capacity
data["items"] = [OrderedDict([("weight", weights[i]), ("value", values[i])]) for i in range(nObjects)]

Compilation.string_data = "-" + "-".join(str(v) for v in (nObjects, capacity, "{:02d}".format(seed)))
