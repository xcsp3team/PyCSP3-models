"""
Layout for electrical components on stripboard.

Taking component footprints, pin locations and pinlist as input and trying to produce the most compact layout.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019/2022 Minizinc challenges.
MIT Licence (Copyright 2022 Monash University, model by Jason Nguyen, for the original MZN model)

## Data Example
  common-emitter-simple.json

## Model
  constraints: AllDifferent, Element, Maximum, NoOverlap, Table

## Execution
  python3 Stripboard.py -data=<datafile.dzn> -parser=Stripboard_ParserZ.py
  python Stripboard.py -data=<datafile.json> -parser=Stripboard_Converter.py
  python Stripboard.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn22, mzn25
"""

from pycsp3 import *

max_w, max_h, nLinks, components, pins, nets = data or load_json_data("common-emitter-simple.json")

full_w = max(max_w, nLinks)

orientation_names = ["Upright", "Clockwise", "UpsideDown", "Anticlockwise"]
nOrientations = len(orientation_names)
Upright, Clockwise, UpsideDown, Anticlockwise = orientations = range(nOrientations)

flat_pins = [u for t in pins for u in t]

footprint_w, footprint_h = [c[1] for c in components], [c[2] for c in components]
pin_dx, pin_dy = [p[1] for p in flat_pins], [p[2] for p in flat_pins]
max_value = max(max(t) for t in (footprint_w, footprint_h, pin_dx, pin_dy))


def component_of(p):
    return next(j for j in range(nComponents) if p < sum(len(t) for t in pins[:j + 1]))


def Tx(p):
    c = component_of(p)
    return [(Upright, pin_dx[p] - 1), (Clockwise, footprint_h[c] - pin_dy[p]), (UpsideDown, footprint_w[c] - pin_dx[p]), (Anticlockwise, pin_dy[p] - 1)]
    # return c


def Ty(p):
    c = component_of(p)
    return [(Upright, pin_dy[p] - 1), (Clockwise, pin_dx[p] - 1), (UpsideDown, footprint_h[c] - pin_dy[p]), (Anticlockwise, footprint_w[c] - pin_dx[p])]


nComponents = len(components)
nPins = len(flat_pins)
nPads = 1 + nPins + nLinks + nLinks
nNets = len(nets)

link_starts = [1 + nPins + l for l in range(nLinks)]
link_ends = [1 + nPins + nLinks + l for l in range(nLinks)]

DUMMY = 0
UNCONNECTED = 0

roots = [0] + [1 + next(j for j in range(nPins) if flat_pins[j][3] == v) for v in nets] + [1 + nPins + nLinks + j for j in range(nLinks)]

link_x = VarArray(size=nLinks, dom=range(1, full_w + 1))
link_y = VarArray(size=nLinks, dom=range(-1, max_h + 1))
link_length = VarArray(size=nLinks, dom=range(1, max_h + 1))

component_x = VarArray(size=nComponents, dom=range(1, max_w + 1))
component_y = VarArray(size=nComponents, dom=range(1, max_h + 1))
component_z = VarArray(size=nComponents, dom=lambda i: [v for v in range(nOrientations) if orientation_names[v] in components[i][3]])  # z for orientation

parent = VarArray(size=nPads, dom=range(nPads))
distance = VarArray(size=nPads, dom=range(nPads))
connection = VarArray(size=nPads, dom=range(nNets + 1))

pad_x = VarArray(size=nPads, dom=range(full_w + 1))
pad_y = VarArray(size=nPads, dom=range(-1, max_h + 1))
pad_xy = VarArray(size=nPads, dom=range((full_w + 1) * (max_h + 1) + full_w))

dx = VarArray(size=nComponents + nLinks, dom=lambda i: footprint_w + footprint_h if i < nComponents else {1})
dy = VarArray(size=nComponents + nLinks, dom=lambda i: footprint_w + footprint_h if i < nComponents else range(2, max_h + 2))

px = VarArray(size=nPins, dom=range(max_value + 1))
py = VarArray(size=nPins, dom=range(max_value + 1))

satisfy(
    # computing dx and dy
    [
        (component_z[c], dx[c], dy[c]) in T for c in range(nComponents)
        if (T := [(v, footprint_w[c], footprint_h[c]) if v in (Upright, UpsideDown) else (v, footprint_h[c], footprint_w[c]) for v in orientations])
    ],

    # merging the two next tables ?
    [(component_z[component_of(p)], px[p]) in Tx(p) for p in range(nPins)],

    [(component_z[component_of(p)], py[p]) in Ty(p) for p in range(nPins)],

    [pad_x[1 + p] == component_x[component_of(p)] + px[p] for p in range(nPins)],

    [pad_y[1 + p] == component_y[component_of(p)] + py[p] for p in range(nPins)],

    # computing pax_xy
    [pad_xy[p] == (full_w + 1) * (pad_y[p] + 1) + pad_x[p] for p in range(nPads)],

    [dy[nComponents + i] == link_length[i] + 1 for i in range(nLinks)],

    # Footprints and jumper links can't overlap and must fit inside board
    NoOverlap(
        origins=zip(component_x + link_x, component_y + link_y),
        lengths=zip(dx, dy)
    ),

    # Jumper link pad placement
    [(
        pad_x[link_starts[l]] == link_x[l],
        pad_y[link_starts[l]] == link_y[l],
        pad_x[link_ends[l]] == link_x[l],
        pad_y[link_ends[l]] == link_y[l] + link_length[l]
    ) for l in range(nLinks)],

    #  Dummy pad to be root of unconnected
    [
        pad_x[DUMMY] == 0,
        pad_y[DUMMY] == -1
    ],

    # Pads with different nets have (room for) trace cuts in between
    [
        If(
            connection[p] != connection[q],
            Then=either(pad_xy[p] - pad_xy[q] > 1, pad_xy[p] - pad_xy[q] < 1)
        ) for p, q in combinations(nPads, 2)
    ],

    # Pins are connected to their nets
    [connection[1 + p] == next(j for j in range(nNets) if nets[j] == flat_pins[p][3]) for p in range(nPins)],

    # Links are connected to their nets or aren't present
    [
        (
            connection[link_starts[l]] == connection[link_ends[l]],
            (connection[link_starts[l]] == UNCONNECTED) == (link_y[l] == -1)
        ) for l in range(nLinks)
    ],

    #  Pads in each net form DAGs
    [
        [(parent[p] == p, distance[p] == 0) for p in range(nPads) if p in roots],
        [(parent[p] != p, distance[p] == distance[parent[p]] + 1) for p in range(nPads) if p not in roots],
        [(connection[parent[p]] == connection[p], pad_y[parent[p]] == pad_y[p]) for p in range(nPads)],
    ],

    # Pads in DAG physically connected
    NoOverlap(
        tasks=[Task(origin=min(pad_xy[parent[p]], pad_xy[p]), length=abs(pad_xy[parent[p]] - pad_xy[p])) for p in range(nPads)]
    ),

    # tag(redundant)
    AllDifferent(pad_xy),

    # tag(symmetry-breaking)
    Decreasing(pad_xy[1 + nPins:1 + nPins + nLinks], strict=True),

    # tag(symmetry-breaking)
    [
        If(
            connection[link_starts[l]] == UNCONNECTED,
            Then=pad_x[link_starts[l]] == nLinks - l
        ) for l in range(nLinks)
    ]
)

minimize(
    (Maximum([component_x[i] + dx[i] for i in range(nComponents)] + [(link_y[i] >= 1) * (link_x[i] + 1) for i in range(nLinks)]) - 1)
    *
    (Maximum([component_y[i] + dy[i] for i in range(nComponents)] + [(link_y[i] + dy[nComponents + i]) for i in range(nLinks)]) - 1)
)
