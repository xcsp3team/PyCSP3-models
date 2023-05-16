"""
From "Constraint Programming in OPL", P. Van Hentenryck, L. Michel, L. Perron, and J.-C. Régin, CP'99

This configuration problem involves putting components of different materials (glass, plastic, steel, wood, and copper)
into bins of various types/colors (red, blue, green), subject to capacity (each bin type has a maximum capacity) and compatibility constraints.
Every component must be placed into a bin and the total number of used bins must be minimized.
The compatibility constraints are:
 - red bins cannot contain plastic or steel
 - blue bins cannot contain wood or plastic
 - green bins cannot contain steel or glass
 - red bins contain at most one wooden component
 - green bins contain at most two wooden components
 - wood requires plastic
 - glass excludes copper
 - copper excludes plastic

Execution:
  python3 Vellino.py -data=Vellino-example.json
"""

from pycsp3 import *

Unusable, Red, Blue, Green = BIN_COLORS = 0, 1, 2, 3  # 0 is a special color 'Unusable' for any empty bin
Glass, Plastic, Steel, Wood, Copper = MATERIALS = 0, 1, 2, 3, 4
nColors, nMaterials = len(BIN_COLORS), len(MATERIALS)

capacities, demands = data
capacities.insert(0, 0)  # unusable bins have capacity 0
maxCapacity, nBins = max(capacities), sum(demands)

# c[i] is the color of the ith bin
c = VarArray(size=nBins, dom=range(nColors))

# p[i][j] is the number of components of the jth material put in the ith bin
p = VarArray(size=[nBins, nMaterials], dom=lambda i, j: range(min(maxCapacity, demands[j]) + 1))

satisfy(
    # every bin with a real colour must contain something, and vice versa
    [(c[i] == Unusable) == (Sum(p[i]) == 0) for i in range(nBins)],

    # all components of each material are spread across all bins
    [Sum(p[:, j]) == demands[j] for j in range(nMaterials)],

    # the capacity of each bin is not exceeded
    [Sum(p[i]) <= capacities[c[i]] for i in range(nBins)],

    # red bins cannot contain plastic or steel
    [(c[i] != Red) | ((p[i][Plastic] == 0) & (p[i][Steel] == 0)) for i in range(nBins)],

    # blue bins cannot contain wood or plastic
    [(c[i] != Blue) | ((p[i][Wood] == 0) & (p[i][Plastic] == 0)) for i in range(nBins)],

    # green bins cannot contain steel or glass
    [(c[i] != Green) | ((p[i][Steel] == 0) & (p[i][Glass] == 0)) for i in range(nBins)],

    # red bins contain at most one wooden component
    [(c[i] != Red) | (p[i][Wood] <= 1) for i in range(nBins)],

    # green bins contain at most two wooden components
    [(c[i] != Green) | (p[i][Wood] <= 2) for i in range(nBins)],

    # wood requires plastic
    [(p[i][Wood] == 0) | (p[i][Plastic] > 0) for i in range(nBins)],

    # glass excludes copper
    [(p[i][Glass] == 0) | (p[i][Copper] == 0) for i in range(nBins)],

    # copper excludes plastic
    [(p[i][Copper] == 0) | (p[i][Plastic] == 0) for i in range(nBins)],

    # tag(symmetry-breaking)
    [LexIncreasing(p[i], p[i + 1]) for i in range(nBins - 1)]
)

minimize(
    # minimizing the number of used bins
    Sum(c[i] != Unusable for i in range(nBins))
)

""" Comments
1) writing capacities = [0] + capacities is not possible because the new built list 
   is there not from the specific type of list we need. One would need to call
   the function cp_array

2) posting a LexMatrix does not seem to be correct from the perspective of the model
   (to be checked)
"""
