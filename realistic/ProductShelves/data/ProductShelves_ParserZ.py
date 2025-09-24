from pycsp3.problems.data.parsing import *

skip_empty_lines("%")

data['nAvailableShelves'] = nShelves = number_in(line())
shelves_dimensions = numbers_in(next_line())

ln = next_line()
assert ln.startswith("Product = P(")
ns = numbers_in(ln)
assert len(ns) == 2 and ns[0] == 1
nProductTypes = ns[1]

next_line()
product_dimensions = [numbers_in(next_line())[1:] for _ in range(nProductTypes)]
data['dimensions'] = OrderedDict([("shelves", shelves_dimensions), ("products", product_dimensions)])

next_line()
data['nProductsToBuild'] = numbers_in(next_line())
assert len(data['nProductsToBuild']) == nProductTypes
