from pycsp3.problems.data.parsing import *

nSamples = number_in(line())
nVars = number_in(next_line())
data['maxErrors'] = number_in(next_line())
s = next_line()
while not next_line().endswith(";"):
    s += " " + line()
s += " " + line()
data['sampleOutputs'] = [0 if v == "false" else 1 for v in s[s.index("[") + 1:s.rindex("]")].split(", ")]
assert nSamples == len(data['sampleOutputs'])
s = next_line()
while not next_line().endswith(";"):
    s += " " + line()
s += " " + line()
data['sampleInputs'] = split_with_rows_of_size([0 if v == "false" else 1 for v in s[s.index("[") + 1:s.rindex("]")].split(", ")], nVars)
assert nSamples == len(data['sampleInputs']) and all(len(row) == nVars for row in data['sampleInputs'])

