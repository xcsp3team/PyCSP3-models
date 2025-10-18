from pycsp3.problems.data.parsing import *

l = line()
data['features'] = features = l[l.index("'") + 1:l.rindex("'")].split("', '")
data['nItems'] = nItems = number_in(next_line())
data['db'] = [numbers_in(next_line()) for _ in range(nItems)]
s = next_line()
s = s[s.index("'") + 1:s.rindex("'")]
assert s == features[-1]  # assumption in the model
