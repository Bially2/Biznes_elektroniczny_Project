#!/bin/bash

VPN_DIR="/etc/eti-vpn"

if [ "$1" = "--vpn" ]; then
    echo "Inicjalizacja VPN..."

   
    if [ -d "$VPN_DIR" ]; then
       
        cd "$VPN_DIR"
        
      
        sudo openvpn --config vpnWETI.ovpn --auth-user-pass vpnWETI.user --daemon
        
        echo "Czekam 5 sekund na zestawienie połączenia sieciowego..."
        sleep 5
    else
        echo "Błąd: Nie znaleziono katalogu VPN w $VPN_DIR"
        exit 1
    fi
fi

echo "Łączenie z węzłem Hadoop..."
ssh -t -J rsww@172.20.83.101 hdoop@10.40.71.115 "cd /opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_192914 && exec bash"