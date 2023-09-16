
# Problem RLFAP

## Description
The Radio Link Frequency Assignment Problem (RLFAP) is described in this [paper](https://link.springer.com/content/pdf/10.1023/A:1009812409930.pdf). 
It was the subject of the [2001 ROADEF challege](https://www.roadef.org/challenge/2001/en/). 


## Data
Data can be found in the archive that contains 25 JSON files.
Each instance is defined by a JSON object with 5 main fields (domains, vars, ctrs, interferenceCosts, mobilityCosts).


## Model(s)

There are 3 variants according to  the way optimization must be conducted (called card, span, max).

*Involved Constraints*: [Intension](https://pycsp.org/documentation/constraints/Intension/), [Maximum](https://pycsp.org/documentation/constraints/Maximum/), [NValues](https://pycsp.org/documentation/constraints/NValues/), [Sum](https://pycsp.org/documentation/constraints/Sum/),



## Command Line

```shell
python3 Rlfap.py -data=Rlfap-card-scen-04.json -variant=card [-solve]
python3 Rlfap.py -data=Rlfap-span-scen-05.json -variant=span [-solve]
python3 Rlfap.py -data=Rlfap-max-graph-06.json -variant=max [-solve]
```

## Some Results

All results are available in several tables of the [seminal paper](https://link.springer.com/content/pdf/10.1023/A:1009812409930.pdf).
You can find here some of them: 


| Data                    | Optimum |
|-------------------------|---------|
| Rlfap-card-scen-04.json | 46      |
| Rlfap-span-scen-05.json | 792     |
| Rlfap-max-graph-06.json | 3389    |


