#!/bin/sh
set -v
for file in list*.gv; do
    [ -f "$file" ] || break
    echo $file
    dot -Tpng $file > $file.png
done
convert list*.png -append adjlist.png
rm *.gv
rm list*.png
