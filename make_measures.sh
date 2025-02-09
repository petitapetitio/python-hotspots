
radon cc . -j -O complexity.json

cloc . --match-f='\.py$' --by-file --csv --out=loc.csv

git log --format=format: --name-only --since=12.month \
    | egrep -v '^$'  \
    | sort \
    | uniq -c  \
    | egrep "\.py$" \
    | sort -nr \
    | awk 'BEGIN {print "filename,churn"} {gsub(/^[ \t]+/, "", $0); print $2","$1}' \
    > churn.csv
