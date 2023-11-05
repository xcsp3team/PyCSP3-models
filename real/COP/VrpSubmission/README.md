# Problem VrpSubmission
## Description
Capacitated Vehicle Routing problem with Time Windows, Service Times and Pickup and deliveries.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The MZN model was proposed by Haakon H. Rød (with a Copyright that seems to be like a MIT Licence),
based on Andrea Rendl's work from 2015 and the Routing model used by the LNS solver for VRPs in Google's OR Tools.

## Data
  toy-D-2v-4l-w-reload.json

## Model
  constraints: [Circuit](http://pycsp.org/documentation/constraints/Circuit), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python VrpSubmission.py -data=file.json

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn21
