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
  realistic, mzn20
"""

from pycsp3 import *

weights, links, nodes, start_domain, target_domain, vnflist, vnf_arcs, proximity_to_source, proximity_to_destination, domain_constraints = data
nDomains, nLinks, nNodes, nVnfs = len(weights), len(links), len(nodes), len(vnflist)

TYPE, DOMAIN, GATEWAY, ENDPOINT = 1, 7, 8, 9

L = [(i, (nodes[links[i][0]], nodes[links[i][1]])) for i in range(nLinks)]
G = [(i, (a, b)) for i, (a, b) in L if a[TYPE] == b[TYPE] == GATEWAY]
Gr = [i for i, _ in G]


def dp(i, j):
    l1 = [sl[k] for k, (a, b) in G if b[DOMAIN] == i and a[DOMAIN] == j]
    l2 = [sl[k] & pth[a[DOMAIN]][j] for k, (a, b) in G if b[DOMAIN] == i and a[DOMAIN] != j]
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
            Then=Sum(
                both(
                    nodes[vnf[j]][DOMAIN] == i,
                    nodes[vnf[j]][TYPE] == t
                ) for j in range(nVnfs)
            ) in range(mi, ma + 1)
        ) for i, t, mi, ma in domain_constraints
    ],

    # any domain has a path to itself
    [pth[i][i] == 1 for i in range(nDomains)],

    # propagating domain path
    [pth[i][j] == dp(i, j) for i, j in combinations(nDomains, 2)],

    # first element in matching (start ENDPOINT)
    [vnf[0] == i for i, a in enumerate(nodes) if a[DOMAIN] == start_domain and a[TYPE] == ENDPOINT],

    # final element in matching (target ENDPOINT)
    [vnf[-1] == i for i, a in enumerate(nodes) if a[DOMAIN] == target_domain and a[TYPE] == ENDPOINT],

    # node type in matching observes vnflist
    [
        Exist(
            vnf[i] == j for j, b in enumerate(nodes) if b[TYPE] == vnflist[i]
        ) for i in range(1, nVnfs)
    ],

    # bound vnf to selected nodes (arcs)
    [
        Exist(
            both(sl[j] == 1, vnf[i] == links[j][1]) for j in range(nLinks)
        ) for i in range(1, nVnfs)
    ],

    # bound vnf to path
    [pth[nodes[vnf[i]][DOMAIN], nodes[vnf[j]][DOMAIN]] == 1 for i, j in vnf_arcs],

    # proximity constraints
    (
        [
            Exist(
                both(sn[j] == 1, vnf[i] == j) for j, b in enumerate(nodes) if b[DOMAIN] == target_domain
            ) for i in range(nVnfs) if proximity_to_destination[i] == 1
        ],
        [
            Exist(
                both(sn[j] == 1, vnf[i] == j) for j, b in enumerate(nodes) if b[DOMAIN] == start_domain
            ) for i in range(nVnfs) if proximity_to_source[i] == 1
        ]
    ),

    # node with incoming arc means node domain is selected
    [
        If(
            sl[i],
            Then=[
                sd[a[DOMAIN]],
                sd[b[DOMAIN]],
                sn[links[i][0]],
                sn[links[i][1]]
            ]
        ) for i, (a, b) in L
    ],

    # getting the number of fun nodes by filtering selected_nodes
    nf == Sum(sn[i] for i in range(nNodes) if nodes[i][TYPE] != GATEWAY),

    # # tightly bounding the number of selected fun nodes
    nf == nVnfs,

    # ENDPOINT arcs must be selected in start and target domains
    [sl[i] == 1 for i, (a, b) in L if
     (b[TYPE] == GATEWAY and a[TYPE] == ENDPOINT and a[DOMAIN] == start_domain) or (a[TYPE] == GATEWAY and b[TYPE] == ENDPOINT and b[DOMAIN] == target_domain)],

    # no arcs to ENDPOINT if they are not start target domains
    [sl[i] == 0 for i, (a, b) in L if (a[TYPE] == ENDPOINT and a[DOMAIN] != start_domain) or (b[TYPE] == ENDPOINT and b[DOMAIN] != target_domain)],

    # ENDPOINT in start and target domains are selected, others no
    [sn[i] == (1 if a[DOMAIN] in (start_domain, target_domain) else 0) for i, a in enumerate(nodes) if a[TYPE] == ENDPOINT],

    # no loop between neighbor domains
    [
        either(
            sl[i] != 1,
            sl[j] != 1
        ) for i, j, in combinations(Gr, 2) if links[i][0] == links[j][1] and links[i][1] == links[j][0]
    ],

    # start domain has no incoming arc from other domain
    [sl[i] == 0 for i, (a, b) in L if a[TYPE] == b[TYPE] == GATEWAY and b[DOMAIN] == start_domain],

    #  no domains allow 2 incoming arcs from different domains
    [
        either(
            sl[i] != 1,
            sl[j] != 1
        ) for (i, (a, b)), (j, (c, d)) in combinations(G, 2) if b[DOMAIN] == d[DOMAIN] and a[DOMAIN] != c[DOMAIN]
    ],

    # each selected domain must have an incoming arc from other domain
    [
        If(
            sd[i] == 1,
            Then=Exist(sl[j] for j, (a, b) in G if b[DOMAIN] == i and a[DOMAIN] != i)
        ) for i in range(nDomains) if i != start_domain
    ],

    # no outgoing arcs from unselected domains
    [
        If(
            sd[a[DOMAIN]] == 0,
            Then=sl[i] == 0
        ) for i, (a, b) in L
    ],
)

minimize(
    Sum(weights[a[DOMAIN]][b[DOMAIN]] * sl[i] for i, (a, b) in G)
)
