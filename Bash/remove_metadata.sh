#!/bin/bash

file=$1

exiftool -all= -overwrite_original $file

echo "Usunieto metadane z pliku $file"
