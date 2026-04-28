#!/bin/bash

#zmienne pomocnicze
state_file="/home/frodz/lab_programowanie_sc/logi_ssh/monitor_state.txt"

report="/home/frodz/lab_programowanie_sc/logi_ssh/ssh_report.txt"

#sprawdzamy kiedy ostatni raz sprawdzano logi
if [[ -f "$state_file" ]]; then
   #jesli istnieje, program odczyta zapisany czas
   new_logs=$(cat "$state_file")
else
    #jesli nie istnieje, przyjmujemy domysle ostania godzine
    new_logs="1 hour ago"
fi

#pobieramy logi ssh od ostatniego sprawdzenia
log_file=$(journalctl -u ssh --no-pager --since "$new_logs")

#zliczenie niepoprawnych prob logowan
failed_login=$(echo "$log_file" | grep "Failed password" | wc -l)

#pozyskanie adresow ip, z nieudanych prob logowania
ips=$(echo "$log_file" | grep "Failed password" | grep -oE 'from [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | awk '{print $2}' | sort | uniq)

#zapisujemy raport, jezeli wystapily nieudane proby
if [[ $failed_login -gt 0 ]]; then
{
	echo "=== RAPORT: $(date) ==="
	echo "Liczba nieudanych logowan: $failed_login"
	echo
	echo "Nieudane logowania z IP:"
	echo "$ips"
	echo

} >> "$report"
else
#informujemy, ze nie wystapily nieudane proby logowania
echo "Nie wykryto nieudanych prob logowania"
fi

#aktualizujemy czas ostaniego sprawdzenia teraz
date +"%Y-%m-%d %H:%M:%S" > "$state_file"

