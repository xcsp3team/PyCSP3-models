from pycsp3.problems.data.parsing import *

# python3 HCPizza.py -data=tiny.txt -dataparser=HCPizza_Parser.py

nRows = next_int()
next_int()  # nCols
data["minIngredients"] = next_int()
data["maxSize"] = next_int()
data["pizza"] = [[0 if c == "M" else 1 for c in line if c != '\n'] for line in remaining_lines()]
