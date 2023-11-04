#!/bin/csh
# usage ./import_from_ppycsp.sh model [academic|real|recreational] [CSP|COP]
# ./_private/import_from_ppycsp.sh  ../ppycsp3/pproblems/mzn08/DeBruijn.py academic CSP
set file = `basename $1:r`
set dir = ./$2/$3/$file
mkdir $dir
cp $1 $dir
python _private/readme.py $dir/$file.py
