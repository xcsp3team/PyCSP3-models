#!/bin/csh

foreach file (`find $1 -type d`)
  echo $file
  echo $file:t
  python3 _private/readme.py $file/$file:t.py
end
