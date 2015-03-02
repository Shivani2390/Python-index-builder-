find *.dat | while read name; do
  rm "$name"
done 
gzip "InvertedIndex.txt" ;