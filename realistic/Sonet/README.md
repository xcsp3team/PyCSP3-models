# Problem Sonet
## Description
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

## Data (example)
  s3ring03json

## Model
  constraints: [Lex](http://pycsp.org/documentation/constraints/Lex), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python Sonet.py -data=<datafile.json>
  - python Sonet.py -data=<datafile.txt> -parser=Sonet_Parser.py

## Links
  - https://www.csplib.org/Problems/prob056/
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  real, csplib, xcsp23
