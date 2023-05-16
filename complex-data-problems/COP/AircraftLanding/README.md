# Problem AircraftLanding

## Description
See OR-library

See "Scheduling aircraft landings - the static case" by J.E. Beasley, M. Krishnamoorthy, Y.M. Sharaiha and D. Abramson,
    Transportation Science, vol.34, 2000, pp180-197.

See "Displacement problem and dynamically scheduling aircraft landings" by J.E. Beasley, M. Krishnamoorthy, Y.M. Sharaiha and D. Abramson,
    Journal of the Operational Research Society, vol.55, 2004, pp54-64.
See http://people.brunel.ac.uk/~mastjjb/jeb/orlib/airlandinfo.html

See the model proposed in the Choco Tutorial, where the following short description is taken:
"Given a set of planes and runways, the objective is to minimize the total (weighted) deviation from the target landing time for each plane.
There are costs associated with landing either earlier or later than a target landing time for each plane.
Each plane has to land on one of the runways within its predetermined time windows such that separation criteria between all pairs of planes are satisfied."



## Data
Data are parsed using the parser given in the directory. The archive contains several data.




## Model

*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent) [Extension](https://pycsp.org/documentation/constraints/Extension) [Intension](https://pycsp.org/documentation/constraints/Intension) [Sum](https://pycsp.org/documentation/constraints/Sum) [NoOverlap](https://pycsp.org/documentation/constraints/NoOverlap)


## Command Line

```shell
  python3 AircraftLanding.py -data=airland1.txt -dataparser=AircraftLanding_Parser.py
  python3 AircraftLanding.py -data=airland1.txt -dataparser=AircraftLanding_Parser.py -variant=table
```


