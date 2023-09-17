#!/bin/csh

foreach file (`find $1 -type d`)
  echo $file
  echo $file:t
  python _private/readme.py $file/$file:t.py
end
