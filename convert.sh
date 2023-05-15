
# csh convert.sh problem directory (zero / simple /compex) type (COP/CSP)
# example : csh convert.sh Blackhole complex CSP
set problem = $1
set dir = "$2-data-problems"
set type = $3
set letter = `echo $problem | cut -c1-1`
echo $letter
set old = /home/audemard/public_html/pycsp3-web/models
rm -rf $dir/$type/$problem
mkdir $dir/$type/$problem
more $old/$letter/$problem.md > $dir/$type/$problem/README.md

set git = `more $dir/$type/$problem/README.md |grep -Eo 'https://github[^ >]+' |head -1| cut -d')' -f1 | sed 's/github.com/raw.githubusercontent.com/' |sed 's/blob//'`
wget $git
mv $problem.py  $dir/$type/$problem

# https://github.com/xcsp3team/pycsp3/blob/master/problems/csp/academic/Bibd.py
# https://raw.githubusercontent.com/xcsp3team/pycsp3/master/problems/csp/academic/Bibd.py