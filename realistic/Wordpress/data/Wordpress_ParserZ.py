from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
if line().startswith("WP"):
    data["WPinstance"] = number_in(line())
    data["nWMs"] = number_in(next_line())
    next_line(repeat=1)
else:
    data["WPinstance"] = -1
    data["nWMs"] = -1
nComponents = number_in(line())
assert nComponents == 5
nHardwareRequirements = number_in(next_line(repeat=1))
nOffers = number_in(next_line(repeat=1))
next_line()
offers = [numbers_in(next_line()) for _ in range(nOffers)]
offers.append([0, 0, 0])  # dummy VM added
nOffers += 1
next_line()
data["requirementsPerComponent"] = [numbers_in(next_line()) for _ in range(nComponents)]
assert len(data["requirementsPerComponent"][0]) == nHardwareRequirements
next_line()
data["offers"] = offers
data["prices"] = numbers_in(next_line()) + [0]  # 0 for the dummy VM
assert len(data["prices"]) == nOffers

# python3 Wordpress.py -data=["WP=3","10",0020.dzn] -parser=Wordpress_ParserZ.py
