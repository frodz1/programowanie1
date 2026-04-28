#!/bin/bash

file=$1
filename=$(echo "$file" | cut -d'.' -f1)

openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt -in "$file" -out "$filename.enc" -pass pass:haslo
