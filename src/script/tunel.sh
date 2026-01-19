#!/bin/bash

NODE_NUM="01"

for arg in "$@"
do
    case $arg in
        --vpn)
            echo "Uruchamiam VPN..."
            cd /vpn-eti/vpn2023/
            sudo openvpn --config vpnWETI.ovpn --auth-user-pass vpnWETI.user --daemon
            ;;
        1|2|3|4)
            NODE_NUM="0${arg}"
            ;;
        *)
            
            ;;
    esac
done

TARGET_HOST="student-swarm${NODE_NUM}.maas"

echo "--------------------------------------------------"
echo "Tworzenie tunelu do: $TARGET_HOST na porcie 19290"
echo "Brama SSH: 172.20.83.101"
echo "--------------------------------------------------"

ssh -L 19290:${TARGET_HOST}:19290 rsww@172.20.83.101
