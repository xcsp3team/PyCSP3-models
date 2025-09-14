from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
nReactions = data['nReactions'] = number_in(line())
nMetabolites = number_in(next_line())
nReversibleReactions = number_in(next_line())
ln = next_line()
reactions = [token[1:-1] for token in ln[ln.index('[') + 1:ln.index(']')].split(", ")]
ln = next_line()
metabolites = [token[1:-1] for token in ln[ln.index('[') + 1:ln.index(']')].split(", ")]
assert nReactions == len(reactions) and nMetabolites == len(metabolites)
data['stoichiometryMatrix'] = [numbers_in(next_line()) for _ in range(nMetabolites)]
data['reversibleIndicators'] = [numbers_in(next_line()) for _ in range(nReversibleReactions)]
