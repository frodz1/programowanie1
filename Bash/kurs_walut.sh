#!/bin/bash

read -p "Podaj kod waluty (USD, EUR): " waluta
waluta=${waluta^^}
echo "$waluta"

#ustalenie daty oraz 7 dni do tylu, poniewaz kursy sa tylko podawane w dni robocze

today=$(date +%F)
start=$(date -d "-7 days" +%F)

#pobranie danych API 
response=$(curl -s "https://api.nbp.pl/api/exchangerates/rates/A/${waluta}/${start}/${today}/?format=json")

if echo "$response" | jq -e .rates >/dev/null 2>&1; then
	echo -e "\nKurs waluty $waluta:"
	Dates=()
	Rates=()


#Wydobądź daty i kursy do tablic
	mapfile -t Daty < <(echo "$response" | jq -r '.rates[].effectiveDate')
	mapfile -t Kursy < <(echo "$response" | jq -r '.rates[].mid')

	for ((i=0; i<${#Daty[@]}; i++)); do
	 echo "${Daty[$i]}: ${Kursy[$i]} PLN"
	done

#Obliczenie różnicy
	echo -e "\nRóżnice miedzy dniami:"
	for ((i=1; i<${#Kursy[@]}; i++)); do
	poprzedni=${Kursy[$((i-1))]}
	teraz=${Kursy[$i]}
	roznica=$(echo "$teraz - $poprzedni" | bc -l)
	roznica=$(printf "%.4f" "$roznica")
	echo "${Daty[$((i-1))]} -> ${Daty[$i]}: $roznica PLN"
      done
else
echo "Brak danych ze strony"
fi
