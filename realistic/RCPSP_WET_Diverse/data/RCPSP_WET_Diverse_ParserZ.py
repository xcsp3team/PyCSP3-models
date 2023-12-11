from ppycsp3.pproblems.mzn16.RCPSPWet_ParserZ import *

next_line(repeat=2)
data['earlinessMin'] = number_in(next_line())
data['earlinessMax'] = number_in(next_line())
data['tardinessMin'] = number_in(next_line())
data['tardinessMax'] = number_in(next_line())
data['nSolutions'] = number_in(next_line())
