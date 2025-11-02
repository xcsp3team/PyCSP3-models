"""
From Akgun et al.'s JAIR'25 paper:
    A Strong External Difference Family (SEDF) is an object defined on a group, with applications in communications and cryptography.
    Given a finite group G on a set of size n, an (n,m,k,λ) SEDF is a list A1, ..., Am of disjoint subsets of size k of G such that,
    for all 1 ≤ i ≤ m, the multi-set {xy-1 | x ∈ Ai , y ∈ Aj , i != j} contains λ occurrences of each non-identity element of G.
    The parameters of the SEDF problem are (n,m,k,λ), the group G given as a multiplication table tab (which is an n × n matrix of integers),
    and inv, a one-dimensional table which maps each group element to its inverse.
    The SEDF is represented as an m × k matrix sedf.


The model, below, is close to (can be seen as the close translation of) the one proposed in [Akgun et al. JAIR, 2025].
See Experimental Data for TabID Journal Paper (URL given below).

## Data Example
  19-1-C19-3-3-1.json

## Model
  constraints: AllDifferent, Cardinality, Element

## Execution
  python SEDF.py -data=<datafile.json>
  python SEDF.py -data=<datafile.txt> -parser=SEDF_ParserE.py

## Links
  - https://www.jair.org/index.php/jair/article/view/17032/27165
  - https://pure.york.ac.uk/portal/en/datasets/experimental-data-for-tabid-journal-paper
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

inv, tab, k, m, ld = data or load_json_data("19-1-C19-3-3-1.json")

n = len(inv)

N, M, K = range(n), range(m), range(k)

# x[i][j] is the jth value of the ith list
x = VarArray(size=[m, k], dom=range(1, n + 1))

satisfy(
    # ensuring all different values
    AllDifferent(x),

    [Increasing(x[i], strict=True) for i in M],

    Increasing(x[:, 0], strict=True),

    # ensuring the right number of occurrences
    [
        Cardinality(
            within=[tab[x[i1][j1], inv[x[i2][j2]]] for j1 in K for i2 in M if i1 != i2 for j2 in K],
            occurrences={v + 1: 0 if v == 0 else ld for v in N}
        ) for i1 in M
    ]
)
