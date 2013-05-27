#!/usr/bin/env bash

runTest() {
  wc -c $1
  time ./bin/trix -b 5 -a search $1 data/out
  python3 tools/draw_placement.py data/out $2
}

for i in a b c d e f g; do
  runTest "data/in.$i" "$i.gif"
done