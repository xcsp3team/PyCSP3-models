import json

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

# illustrating how to convert from a JSON format to another one.
# For example python ConcertHall.py -data=test.json -parser=ConcertHall_Converter.py [-export]


name = options.data  # the name of the JSON file whose format must be converted
with open(name) as f:
    d = json.load(f)

starts = d.get("start")
ends = d.get("end")
prices = d.get("price")
requirements = d.get("requirement")
assert d.get("num_offers") == len(starts) == len(ends) == len(prices) == len(requirements)

capacities = d.get("capacity")
assert d.get("num_halls") == len(capacities)

data['capacities'] = capacities
data['concerts'] = [OrderedDict([("start", starts[i]), ("end", ends[i]), ("price", prices[i]), ("requirement", requirements[i])]) for i in range(len(starts))]
