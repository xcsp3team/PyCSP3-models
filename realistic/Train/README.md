# Problem Train

We have n trains moving along a single track with m stations.
There is a non-zero constant flow of passengers arriving at all but the first and last station who wish to travel to the final station.
Trains are originally scheduled so that they collect the passengers and drop them at the final station.
To this original schedule a disruption is introduced whereby a train is delayed.
Each of the trains (at the time of the delay) has knowledge of the duration of the delay.
The objective is to reschedule the trains to minimize the average travel time of the passengers.
Trains are not able to overtake preceding trains, however they do have the option to skip a station and wait longer at a station to collect more passengers.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012/2014/2018 Minizinc challenges.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  01.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Train.py -data=<datafile.json>
  python Train.py -data=<datafile.dzn> -parser=Train_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, mzn12, mzn14, mzn18
