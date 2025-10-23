# Problem: Elitserien

In a 14-team league, form 2 divisions which hold a SRRT (Single Round-Robin Tournament):
  - each 7-team division must hold a SRRT to start the season
  - this must be followed by two SRRTs between the entire league, the second SRRT being a mirror of the first
  - there must be a minimum number of breaks in the schedule (home-home pair or away-away pair)
  - each team has one bye during the season (to occur during the divisional RRT)
  - at no point during the season can the number of home and away games played by a team differ by more than 1
  - any pair of teams must have consecutive meetings occur at different venues (Alternative Venue Requirement)
  - each division must have 3 pairs of complementary schedules

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2016/2018/2023 Minizinc challenges.
The original MZN model was proposed by Jeff Larson and Mats Carlsson, and described in the papers mentioned below.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  handball01.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Channel](https://pycsp.org/documentation/constraints/Channel), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Regular](https://pycsp.org/documentation/constraints/Regular), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Elitserien.py -data=<datafile.json>
  python Elitserien.py -data=<datafile.dzn> -parser=Elitserien_ParserZ.py
```

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0377221716309584?via%3Dihub
  - https://link.springer.com/chapter/10.1007/978-3-319-07046-9_11
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn14, mzn16, mzn18, mzn23
