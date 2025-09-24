# Problem: Coprime

From Akgun et al.'s JAIR'25 paper:
    Erdős and Sárközy studied a range of problems involving coprime sets.
    A pair of numbers a and b are coprime if there is no integer n > 1 which is a factor of both a and b.
    The Coprime Sets problem of size k is to find the smallest m such that there is a subset of k distinct numbers from {m/2 . . . m} that are pairwise coprime.

The model, below, is close to (can be seen as the close translation of) the one proposed in [Akgun et al. JAIR, 2025].
See Experimental Data for TabID Journal Paper (URL given below).

## Data
  a number n

## Execution
```
  python Coprime.py -data=number
  python Coprime.py -data=number -variant=table
```

## Links
  - https://www.jair.org/index.php/jair/article/view/17032/27165
  - https://pure.york.ac.uk/portal/en/datasets/experimental-data-for-tabid-journal-paper
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  academic, xcsp25
