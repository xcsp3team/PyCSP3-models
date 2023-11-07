#!/bin/csh

foreach f (`ls $1`)
echo $f:r
mkdir $1/$f:r
mv $1/$f $1/$f:r
end;
