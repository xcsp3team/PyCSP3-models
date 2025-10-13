"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The original MZN model was proposed by Bogdan David, under the MIT Licence.

## Data Example
  07-500.json

## Model
  constraints: Sum

## Execution
  python Wordpress.py -data=sm-10-13-00.json
  python Wordpress.py -data=sm-10-13-00.dzn -parser=Wordpress_ParserZ.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S2352220821000274
  - https://www.minizinc.org/challenge2022/results2022.html
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  realistic, mzn22, xcsp24
"""

from pycsp3 import *

lbWP, nVMs, requirements, types, prices = data or load_json_data("07-500.json")  # requirements per components, type and price of possible VMs

assert len(requirements) == 5

nComponents, nFeatures = 5, len(requirements[0])  # features are hardware settings (CPU, Memory, Storage)
nTypes = len(types)  # note that a dummy type has been added at last position by the parser

# WP for WordPress, SQL for MySQL, DNS for DNS_LoadBalancer, HTTP for HTTP_LoadBalancer, VS for Varnish Software
WP, SQL, DNS, HTTP, VS = range(nComponents)

# x[i][k] is 1 iff the kth VM is used for the ith component
x = VarArray(size=[nComponents, nVMs], dom={0, 1})

# oc[k] is 1 iff the kth VM is used/occupied (i.e., not a dummy VM)
oc = VarArray(size=nVMs, dom={0, 1})

# tp[k] is the type of the kth chosen VM
tp = VarArray(size=nVMs, dom=range(nTypes))

# pr[k] is the price of the kth chosen VM
pr = VarArray(size=nVMs, dom=range(0, 16001))

satisfy(
    # ensuring certain limits (cardinality) on the deployment of components
    [
        Sum(x[WP]) >= lbWP,
        Sum(x[SQL]) >= 2,
        Sum(x[VS]) >= 2,
        Sum(x[DNS]) <= 1
    ],

    # ensuring used VMs are considered as being occupied
    [oc[k] == (Sum(x[:, k]) > 0) for k in range(nVMs)],

    # tag(symmetry-breaking)
    Decreasing(oc),

    # ensuring that hardware requirements are met for each component
    [x[:, k] * requirements[:, h] <= types[tp[k], h] for k in range(nVMs) for h in range(nFeatures)],

    # computing prices of chosen VMs
    [pr[k] == prices[tp[k]] for k in range(nVMs)],

    # ensuring certain connections between deployment of components
    [
        (Sum(x[DNS]) > 0) != (Sum(x[HTTP]) > 0),
        If(
            Sum(x[DNS]) > 0,
            Then=Sum(x[WP]) <= 7 * Sum(x[DNS]),
            Else=Sum(x[WP]) <= 3 * Sum(x[HTTP])
        ),
        2 * Sum(x[WP]) <= 3 * Sum(x[SQL])
    ],

    # ensuring that conflicting components do not share the same VM
    [
        [x[VS][k] + x[i][k] <= 1 for k in range(nVMs) for i in (DNS, HTTP, SQL)],
        [x[DNS][k] + x[i][k] <= 1 for k in range(nVMs) for i in (WP, SQL, VS)],
        [x[HTTP][k] + x[i][k] <= 1 for k in range(nVMs) for i in (WP, SQL, VS)]
    ]
)

minimize(
    # minimizing overall cost
    Sum(pr)
)

""" Comments
1) The array oc is useful only if we post:
     Decreasing(oc)
   to avoid symmetries
2) When computing prices of chosen VMS, the array oc is useless because of the dummy VM (with price 0)
3) [Sum(x[i]) >= 1 for i in (WP, SQL, VS)], 
   is useless as subsumed by constraints in the first posted group
"""
