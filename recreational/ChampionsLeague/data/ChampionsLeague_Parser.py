from pycsp3.problems.data.parsing import *

lines = remaining_lines()
matches = [[tok.strip() for tok in ln.split("-")] for ln in lines[:-1]]
teams = {team for row in matches for team in row}
assert len(teams) == 36
ordered_teams = sorted(list(teams))
assert all(len([t for row in matches for t in row if t == team]) for team in ordered_teams)
schedule = [[ordered_teams.index(t) for t in row] for row in matches]
schedule = split_with_rows_of_size(schedule, 18)

data["schedule"] = schedule
data["position"] = number_in(lines[-1])
