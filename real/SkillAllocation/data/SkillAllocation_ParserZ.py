from pycsp3.problems.data.parsing import *

data['nNewSkills'] = number_in(line())
data['nMaxJobs'] = number_in(next_line())
assert data['nMaxJobs'] > 0
nSkills = len(next_line().split(",")) - 1
next_line()
data['engineerSkills'] = split_with_rows_of_size(numbers_in(line()), nSkills)
data['engineerLocations'] = numbers_in(next_line())
jobs = split_with_rows_of_size(numbers_in(next_line()), 5)
for job in jobs:
    job[0] -=1
data['jobs'] = jobs