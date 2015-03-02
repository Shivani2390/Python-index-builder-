#!/bin/sh
#echo "$1"
mv "$1" "$1.gz";
gzip -d "$1.gz" ;
