#!/bin/bash
#zad 1.1
mkdir $1
mkdir $2
#zad1.2
cd $1
mkdir A1
mkdir A1/A11
mkdir B1
mkdir B1/B11.1
mkdir C
touch ./A1/t1.txt
touch ./B1/B11.1/f1.csv
touch ./C/ccc.txt
cd ~
#zad1.3
cd $2
mkdir 1A
mkdir 1B
touch 1A/x.txt
touch 1B/1234.csv
cd ~
#zad1.4
mv ~/$1/A1/t1.txt ~/$2/1A
#zad1.5
cp ~/$1/B1/B11.1/f1.csv ~/$2/1B/
#zad1.6
mv ~/$1/A1 ~/$1/Aa1
#zad1.7
cd $1
#zad1.8
ls -lR | grep "^d.*[12]$"
#zad1.9
du -h --max-depth=1
#zad1.10
tree -h
#zad1.11
pwd
#zad1.12
readlink -f .
#zad1.13
cd ..
#zad1.14
cp -r ~/$1 ~/$2
#zad.1.15
rm -r ~/$1
#zad1.16
tar -czvf 283825_lab0.tar.gz ~/$2
