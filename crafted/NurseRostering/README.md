# Problem NurseRostering
## Description
This problem was described in the JAIR paper cited below.

This problem was inspired by a rostering context.
The objective is to schedule n employees over a span of n time periods.
In each time period, n−1 tasks need to be accomplished and one employee out of the n has a break.
The tasks are fully ordered 1 to n−1; for each employee the schedule has to respect the following rules:
  - two consecutive time periods have to be assigned to either two consecutive tasks, in no matter which order i.e. (t, t+1) or (t+1, t),
    or to the same task i.e. (t, t);
- an employee can have a break after no matter which task;
- after a break an employee cannot perform the task that precedes the task prior to the break, i.e. (t, break, t−1) is not allowed.
The problem is modeled with one Regular constraint per row and one Alldifferent constraint per column.

The model/automaton below is made stricter so as (hopefully) to generate harder instances.

## Data
  roster-5-00-01.dat

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Regular](http://pycsp.org/documentation/constraints/Regular)

## Execution
  - python NurseRostering.py -data=<datafile.json>
  - python NurseRostering.py -data=<datafile.dat> -parser=NurseRostering_Parser.py

## Links
  - https://dl.acm.org/doi/abs/10.5555/2387915.2387920
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  crafted, xcsp22
