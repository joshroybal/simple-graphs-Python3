#!/bin/sh
set -v
./debug.py 8
#dot -Tpng graph.gv > graph.png
#geeqie graph.png
for file in list*.gv; do
    [ -f "$file" ] || break
    echo $file
    dot -Tpng $file > $file.png
done
convert list*.png -append adjlist.png
rm *.gv
rm list*.png
geeqie adjlist.png
