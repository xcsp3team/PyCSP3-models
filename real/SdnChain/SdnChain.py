"""
Service Function Chain.

The problem is to deliver end-to-end networking services across multiple network domains
by implementing the so-called Service Function Chain (SFC) i.e., a sequence of Virtual Network Functions (VNF)
that composes the service.
See paper link below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
It seems that the original MZN model was proposed by Liu, Tong, et al.
No Licence was explicitly mentioned (MIT Licence is assumed).

NB: We obtain the same bounds for all instances except for the instance d30 where we get 22 (with ACE and Choco) instead of 23.
After double checking, we didn't find what is the difference between the two models
TODO : problem with an instance (bound)

## Data Example
  d10n780-1.json

## Model
  constraints: Count, Element, Sum

## Execution
  python SdnChain.py -data=<datafile.json>
  python SdnChain.py -data=<datafile.dzn> -parser=SdnChain_ParserZ.py

## Links
  - https://inria.hal.science/hal-02395208
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, mzn20
"""

from pycsp3 import *

weights, links, nodes, start_domain, target_domain, vnflist, vnf_arcs, proximity_to_source, proximity_to_destination, domain_constraints = data
nDomains, nLinks, nNodes, nVnfs = len(weights), len(links), len(nodes), len(vnflist)

TYPE = 1
DOMAIN = 7
GATEWAY = 8
ENDPOINT = 9

inds = [i for i in range(nLinks) if nodes[links[i][0], TYPE] == nodes[links[i][1], TYPE] == GATEWAY]


def sel(i, j, s, equal):
    a, b = links[s]
    return nodes[a][TYPE] == nodes[b][TYPE] == GATEWAY and nodes[b][DOMAIN] == i and equal == (nodes[a][DOMAIN] == j)


def dp(i, j):
    l1 = [sl[s] for s in range(nLinks) if sel(i, j, s, True)]
    l2 = [sl[s] & pth[k][j] for s in range(nLinks) if sel(i, j, s, False) and [k := nodes[links[s][0]][DOMAIN]]]
    if len(l1) == 0 and len(l2) == 0:
        return 0
    if len(l1) == 0:
        return Count(l2) >= 1
    if len(l2) == 0:
        return Count(l1) >= 1
    return (Count(l1) >= 1) | (Count(l2) >= 1)


# vnf[i] is the (ground) node of the ith VNF
vnf = VarArray(size=nVnfs, dom=range(nNodes))

# pth[i][j] is 1 if domain i is reachable from j (exists a path from j to i)
pth = VarArray(size=[nDomains, nDomains], dom={0, 1})

# sd[i] is 1 if the ith domain is selected, ie traversed by SFC
sd = VarArray(size=nDomains, dom={0, 1})

# sn[i] is 1 if the ith node is selected, ie belongs to SFC
sn = VarArray(size=nNodes, dom={0, 1})

# sl[i] is 1 if the ith link is selected/used
sl = VarArray(size=nLinks, dom={0, 1})

# nf is the number of functional nodes in SFC (excepting GATEWAY nodes)
nf = Var(dom=range(nNodes + 1))

satisfy(

    # ensuring domain VNF
    [
        If(
            sd[i] == 1,
            Then=Sum(both(nodes[vnf[j], DOMAIN] == i, nodes[vnf[j], TYPE] == t) for j in range(nVnfs)) in range(mi, ma + 1)
        ) for i, t, mi, ma in domain_constraints
    ],

    # any domain has a path to itself
    [pth[i][i] == 1 for i in range(nDomains)],

    # propagating domain path
    [pth[i][j] == dp(i, j) for i, j in combinations(nDomains, 2)],

    # first element in matching (start ENDPOINT)
    [vnf[0] == i for i in range(nNodes) if nodes[i][DOMAIN] == start_domain and nodes[i][TYPE] == ENDPOINT],

    # final element in matching (target ENDPOINT)
    [vnf[-1] == i for i in range(nNodes) if nodes[i][DOMAIN] == target_domain and nodes[i][TYPE] == ENDPOINT],

    # node type in matching observes vnflist
    [Exist(vnf[i] == j for j in range(nNodes) if nodes[j][TYPE] == vnflist[i]) for i in range(1, nVnfs)],

    # bound vnf to selected nodes (arcs)
    [Exist(both(sl[j] == 1, vnf[i] == links[j][1]) for j in range(nLinks)) for i in range(1, nVnfs)],

    # bound vnf to path
    [pth[nodes[vnf[a]][DOMAIN], nodes[vnf[b]][DOMAIN]] == 1 for a, b in vnf_arcs],

    # proximity constraints
    (
        [Exist(both(sn[j] == 1, vnf[i] == j) for j in range(nNodes) if nodes[j][DOMAIN] == target_domain)
         for i in range(nVnfs) if proximity_to_destination[i] == 1],
        [Exist(both(sn[j] == 1, vnf[i] == j) for j in range(nNodes) if nodes[j][DOMAIN] == start_domain)
         for i in range(nVnfs) if proximity_to_source[i] == 1]
    ),

    # node with incoming arc means node domain is selected
    [
        If(
            sl[i], Then=[
                sd[nodes[a][DOMAIN]],
                sd[nodes[b][DOMAIN]],
                sn[a],
                sn[b]
            ]
        ) for i, (a, b) in enumerate(links)
    ],

    # getting the number of fun nodes by filtering selected_nodes
    nf == Sum(sn[i] for i in range(nNodes) if nodes[i][TYPE] != GATEWAY),

    # # tightly bounding the number of selected fun nodes
    nf == nVnfs,

    # ENDPOINT arcs must be selected in start and target domains
    [sl[i] == 1 for i, (a, b) in enumerate(links) if
     (nodes[b][TYPE] == GATEWAY and nodes[a][TYPE] == ENDPOINT and nodes[a][DOMAIN] == start_domain)
     or (nodes[a][TYPE] == GATEWAY and nodes[b][TYPE] == ENDPOINT and nodes[b][DOMAIN] == target_domain)],

    # no arcs to ENDPOINT if they are not start target domains
    [sl[i] == 0 for i, (a, b) in enumerate(links) if
     (nodes[a][TYPE] == ENDPOINT and nodes[a][DOMAIN] != start_domain)
     or (nodes[b][TYPE] == ENDPOINT and nodes[b][DOMAIN] != target_domain)],

    # ENDPOINT in start and target domains are selected, others no
    [sn[i] == (1 if nodes[i][DOMAIN] in (start_domain, target_domain) else 0) for i in range(nNodes) if nodes[i][TYPE] == ENDPOINT],

    # no loop between neighbor domains
    [(sl[i] != 1) | (sl[j] != 1) for i, j in combinations(inds, 2) if links[i][0] == links[j][1] and links[i][1] == links[j][0]],

    # start domain has no incoming arc from other domain
    [sl[i] == 0 for i, (a, b) in enumerate(links) if nodes[a][TYPE] == nodes[b][TYPE] == GATEWAY and nodes[b][DOMAIN] == start_domain],

    #  no domains allow 2 incoming arcs from different domains
    [(sl[i] != 1) | (sl[j] != 1) for i, j in combinations(inds, 2)
     if nodes[links[i][1], DOMAIN] == nodes[links[j][1], DOMAIN] and nodes[links[i][0], DOMAIN] != nodes[links[j][0], DOMAIN]],

    # each selected domain must have an incoming arc from other domain
    [
        If(
            sd[i] == 1,
            Then=Exist(sl[j] for j in inds if nodes[links[j][1], DOMAIN] == i and nodes[links[j][0], DOMAIN] != i)
        ) for i in range(nDomains) if i != start_domain
    ],

    # no outgoing arcs from unselected domains
    [
        If(
            sd[nodes[links[i][0], DOMAIN]] == 0,
            Then=sl[i] == 0
        ) for i in range(nLinks)
    ],
)

minimize(
    Sum(weights[nodes[a][DOMAIN], nodes[b][DOMAIN]] * sl[i] for i, (a, b) in enumerate(links) if nodes[a][TYPE] == nodes[b][TYPE] == GATEWAY)
)
