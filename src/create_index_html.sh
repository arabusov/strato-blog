#!/bin/bash
DEPLOYDIR=$1
cat head.html
echo "<h2>Andrei's blog</h2>"
echo "Entries:"
echo "<ul>"
for F in $DEPLOYDIR/*.html; do
    BN=$(basename $F)
    if [[ "$BN" != "index.html" ]]; then
        BNSHORT=${BN%.html}
        echo "<li> <a href=$BN>$BNSHORT</a></li>"
    fi
done
echo "</ul>"
cat tail.html
