#!/bin/bash

#Katalog tymczasowy na archiwum
BACKUP_DIR="/$HOMP/backup"

# Nazwa archiwum z datą
BACKUP_FILENAME="backup_$(date +%Y-%m-%d_%H-%M-%S).tar.gz"
BACKUP_PATH="/home/frodz/lab_programowanie_sc/backup"
FILES_TO_BACKUP="/home/frodz/lab_programowanie_sc/backup"



# Dane FTP (twój komputer jako serwer FTP)
FTP_HOST="127.0.0.1"       # lub np. 192.168.1.10
FTP_USER="ftpuser"
FTP_PASS="ftpuser"
FTP_TARGET_DIR="/kopie_zapasowe"

# === PRZYGOTOWANIE ===


# Tworzenie archiwum
tar -czvf "$BACKUP_FILENAME" $BACKUP_PATH

# === WYSYŁKA NA FTP ===
echo "Wysyłanie archiwum na serwer FTP..."
ftp -inv $FTP_HOST <<EOF
user $FTP_USER $FTP_PASS
cd $FTP_TARGET_DIR
put $BACKUP_PATH
bye
EOF

