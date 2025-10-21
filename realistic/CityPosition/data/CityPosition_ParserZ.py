from pycsp3.problems.data.parsing import *

data['nCities'] = number_in(line())
r = number_in(next_line())
next_line()
src = decrement(numbers_in(next_line()))
dst = decrement(numbers_in(next_line()))
distances = numbers_in(next_line())
assert r == len(src) == len(dst) == len(distances)
data['roads'] = [OrderedDict([("src", src[i]), ("dst", dst[i]), ("distance", distances[i])]) for i in range(r)]
