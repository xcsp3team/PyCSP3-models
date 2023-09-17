# Problem ClockTriplet
## Description

The description can be found [here](http://www.f1compiler.com/samples/Dean%20Clark%27s%20Problem.f1.html)

The problem was originally posed by Dean Clark and then presented to a larger audience by Martin Gardner.
The problem was discussed in Dr. Dobbs's Journal, May 2004 in an article  by Timothy Rolfe.
According to the article, in his August 1986 column for Isaac Asimov's Science Fiction Magazine,
Martin Gardner presented this problem:
Now for a curious little combinatorial puzzle involving the twelve numbers on the face of a clock.
Can you rearrange the numbers (keeping them in a circle) so no triplet of adjacent numbers has a sum higher
than 21? This is the smallest value that the highest sum of a triplet can have.

Timothy Rolfe solves the problem using a rather complex algorithm and also presents a generic algorithm
for numbers other than 12 (clock numbers) and 21 (highest sums of triplets).
The main emphasis of the algorithm was put on the computational speed.
The article stressed the fact that a simple backtracking algorithm would be simply too slow
due to the number of permutations.

The model here is given in a general form.


## Data
A couple [r,n], where r is the size of the tuple (by default triplet) and n the number of hours (by default 12).

## Model(s)

  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Intension](http://pycsp.org/documentation/constraints/Intension)

## Command Line

```
python ClockTriplet.py -data=[3,12]
```

## Tags
 academic
