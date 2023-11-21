#!/bin/csh
# usage ./import_from_ppycsp.sh model [academic|real|recreational]
# ./_private/import_from_ppycsp.sh  ../ppycsp3/pproblems/mzn08/DeBruijn.py academic
set file = `basename $1:r`
set original_dir = $1:h
echo $original_dir
set dir = ./$2/$file
mkdir $dir
mkdir $dir/data
cp $1 $dir
cp $original_dir/"$file"_ParserZ.py $dir/data
python _private/readme.py $dir/$file.py
