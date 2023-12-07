from pycsp3.problems.data.parsing import *

costs = numbers_in(line())
nCategories = number_in(next_line())
l = next_line()
# print(l)
data['domainTypes'] = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("},{")]
assert nCategories == len(data['domainTypes'])
minFreq = number_in(next_line())
maxFreq = number_in(next_line())
nVariables = number_in(next_line())
data['domains'] = decrement(numbers_in(next_line()))
assert nVariables == len(data['domains'])
data['minFreq'] = minFreq
data['maxFreq'] = maxFreq
nHards = number_in(next_line())
hardx = decrement(numbers_in(next_line()))
hardy = decrement(numbers_in(next_line()))
hardk = numbers_in(next_line())
assert nHards == len(hardx) == len(hardy) == len(hardk)
data['hards'] = [(hardx[i], hardy[i], hardk[i]) for i in range(nHards)]
nSofts = number_in(next_line())
softx = decrement(numbers_in(next_line()))
softy = decrement(numbers_in(next_line()))
softk = numbers_in(next_line())
softw = decrement(numbers_in(next_line()))
assert nSofts == len(softx) == len(softy) == len(softk) == len(softw)
data['softs'] = [(softw[i], softx[i], softy[i], softk[i]) for i in range(nSofts)]
data['costs'] = costs
