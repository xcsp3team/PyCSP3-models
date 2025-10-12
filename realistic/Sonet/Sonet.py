"""
This is Problem 064 on CSPLib, called Synchronous Optical Networking Problem (SONET).

In the SONET problem we are given a set of nodes, and for
each pair of nodes we are given the demand (which is the number of channels required to carry
network traffic between the two nodes). The demand may be zero, in which case the two nodes
do not need to be connected. A SONET ring connects a set of nodes. A node is installed on
a ring using a piece of equipment called an add-drop multiplexer (ADM). Each node may be
installed on more than one ring. Network traffic can be transmitted from one node to another
only if they are both installed on the same ring. Each ring has an upper limit on the number
of nodes, and a limit on the number of channels. The demand of a pair of nodes may be split
between multiple rings. The objective is to minimize the total number of ADMs used while
satisfying all demands.

## Data Example
  s2ring02.json

## Model
  constraints: Lex, Sum, Table

## Execution
  python Sonet.py -data=<datafile.json>
  python Sonet.py -data=<datafile.txt> -parser=Sonet_Parser.py

## Links
  - https://www.csplib.org/Problems/prob056/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, csplib, xcsp23
"""

from pycsp3 import *

nNodes, nRings, r, connections = data or load_json_data("s2ring02.json")

# x[i][k] is 1 if the ith ring contains the kth node
x = VarArray(size=[nRings, nNodes], dom={0, 1})

T = {tuple(1 if j // 2 == i else ANY for j in range(2 * nRings)) for i in range(nRings)}

satisfy(
    [x[:, kq] in T for kq in connections],  # kq is a pair of nodes

    # respecting the capacity of rings
    [Sum(x[i]) <= r for i in range(nRings)],

    # tag(symmetry-breaking)
    LexIncreasing(x)
)

minimize(
    # minimizing the number of nodes installed on rings
    Sum(x)
)

""" Comments
1) Note that
  [x[:, kq] in T for j in connections],
 is a shortcut for; 
   [(x[i][kq] for i in range(m)) in T for kq in connections]
 which, itself is a shortcut for:
   [(x[i][k if p == 0 else q] for i in range(m) for p in range(2)) in T
      for (k, q) in connections]
"""
