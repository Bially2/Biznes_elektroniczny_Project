#!/bin/bash

BASTION_USERNAME=rsww
BASTION_SERVER=172.20.83.101
SWARM_USERNAME=hdoop
SWARM_SERVER=student-swarm01.maas

DEST_FOLDER="/opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_192914"

if [ "$#" -ne 2 ]; then
    echo "Użycie: bash wyslij.sh <plik_zrodlowy> <nazwa_docelowa>"
    exit 1
fi

SOURCE_FILE="$1"
DEST_FILE="$2"

echo "Przesyłam $SOURCE_FILE do $DEST_FOLDER/$DEST_FILE..."

scp -o ProxyJump="$BASTION_USERNAME"@"$BASTION_SERVER" "$SOURCE_FILE" "$SWARM_USERNAME"@"$SWARM_SERVER":"$DEST_FOLDER/$DEST_FILE"