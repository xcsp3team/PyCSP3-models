# Problem: FoxGeeseCorn

This is a generalization of the famous Fox-Goose-Corn puzzle. In this version, a farmer
wants to transport some foxes, geese and bags of corn from the west to the east side of a
river. She has a boat with a capacity available for her to move some of the goods at once
while the rest remain on shore. She can go back and forth to bring as many goods as she
wants to the east. Nonetheless, some rules apply to the goods that are not being supervised
on either side while the farmer is on the boat:
  - if only foxes and bags of corn are sitting on a shore, then a fox dies by eating a bag of corn;
  - if there are foxes and geese, and the foxes outnumber the geese, one fox dies;
  - on the other hand, if the geese are not outnumbered, each fox kills one goose;
  - of there is no fox, and the geese outnumber the bags, a goose dies and one bag is eaten;
  - on the other hand, if the corn is not outnumbered, each goose eats a bag.
The farmer must maximize the profit (there is a price for each good) from the surviving
goods on the east.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  a sequence of 8 integers

## Model
  constraints: [Element](https://pycsp.org/documentation/constraints/Element), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python FoxGeeseCorn.py -data=[6,7,8,4,15,8,12,9]
```

## Links
  - https://link.springer.com/article/10.1007/s10601-018-9297-2
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  academic, mzn19, mzn24
