# Problem WarOrPeace
## Description
The problem is described [here](http://www.hakank.org/)

There are n countries.
Each pair of two countries is either at war or has a peace treaty.
Each pair of two countries that has a common enemy has a peace treaty.
What is the minimum number of peace treaties?

The minimum number of peace treaties for n in \[2..12] seems to be floor(n^2/4), (see [https://oeis.org/A002620](https://oeis.org/A002620))

Hence, it is 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81, ...


## Data
A number n,  the number of countries.

## Model(s)

There are two variants.

 cnstraints: Intension, Sum


## Command Line

```
python WarorPeace.py -data=8
python WarorPeace.py -data=8 -variant=or
```

## Tags
 academic
