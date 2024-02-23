"""
Problem 016 on CSPLib

## Data
  all integrated (single problem)

## Execution
  python TrafficLights.py

## Links
 - https://www.csplib.org/Problems/prob016/

## Tags
  single, notebook, csplib
"""

from pycsp3 import *

R, RY, G, Y = "red", "red-yellow", "green", "yellow"

T = {(R, R, G, G), (RY, R, Y, R), (G, G, R, R), (Y, R, RY, R)}

# v[i] is the color for the ith vehicle traffic light
v = VarArray(size=4, dom={R, RY, G, Y})

# p[i] is the color for the ith pedestrian traffic light
p = VarArray(size=4, dom={R, G})

satisfy(
    # ensuring the coherence of traffic lights
    (v[i], p[i], v[i + 1], p[i + 1]) in T for i in range(4)
)

"""
1) Note that auto-adjustment of array indexing is used here. This is equivalent to:
  (v[i], p[i], v[(i + 1) % 4], p[(i + 1) % 4]) in T for i in range(4)
"""
