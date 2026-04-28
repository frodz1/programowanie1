#!/bin/bash

#Komendy, ktore maja sie wykonac
COMMANDS="
echo 'Lista plików:'
ls -lh ~;
echo '';
echo 'Dzialajace procesy:';
ps aux;
"

#Wykonanie polecen przez SSH, wynik zapisany do pliku
ssh "frodz@10.0.2.15" "${COMMANDS}" > "wynik_ssh.txt"

echo "Wyniki zostały zapisane do pliku wynik_ssh.txt"
