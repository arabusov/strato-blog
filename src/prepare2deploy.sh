#!/bin/bash

DEPLOYDIR="./2deploy"
SRCDIR="./articles"
HEAD=head.html
TAIL=tail.html
echo "Clean deploy directory"
rm -rf $DEPLOYDIR
mkdir -p $DEPLOYDIR
cp common.css $DEPLOYDIR
echo "Start convertation"
for i in `ls $SRCDIR`; do
    tex=`basename $i`
    html=`echo $tex | sed 's/\.tex/\.html/g'`
    cat $HEAD > $DEPLOYDIR/$html
    python3 pseudoTeX.py $SRCDIR/$tex >> $DEPLOYDIR/$html
    echo "<a href=index.html>Up</a>" >> $DEPLOYDIR/$html
    cat $TAIL >> $DEPLOYDIR/$html
done
bash create_index_html.sh $DEPLOYDIR > $DEPLOYDIR/index.html
echo "Done."
