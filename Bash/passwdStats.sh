#!/bin/bash

#zad1
mkdir -p $1
#zad2
grep -w "$(whoami)" /etc/passwd
#zad3
cut -d: -f 1,6,7 /etc/passwd | sort -r -t: -k 1,1 > $1/F1.csv
#zad4
cut -d: -f 1 /etc/passwd | rev | sort | rev | uniq > $1/F2.csv
#zad5
cut -d: -f1 /etc/passwd | tr '[:lower:]' '[:upper:]' > $1/F3.txt
#zad6
grep -A 4 -B 4 "$(whoami)" /etc/passwd | grep -v "$(whoami)" > $1/F4.txt
#zad7
diff -y /etc/passwd $1/F4.txt >$1/differences.txt

