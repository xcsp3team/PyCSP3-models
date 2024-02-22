# Problem PSP

This is a particular case of the Discrete Lot Sizing Problem (DLSP); see Problem 058 on CSPLib.

## Data Example
  001.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python PSP1.py -data=<datafile.json>
  - python PSP1.py -data=<datafile.txt> -parser=PSP_Parser.py

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://github.com/xgillard/mznlauncher
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, csplib, xcsp23

<br />

## _Alternative Model(s)_

#### PSP2.py
 - constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)
 - tags: realistic, csplib, xcsp23
