#!/bin/bash

if [ "$1" = "--vpn" ]; then
    
    cd /vpn-eti/vpn2023/
    sudo openvpn --config vpnWETI.ovpn --auth-user-pass vpnWETI.user --daemon [cite: 157, 158]
fi

ssh -t -J rsww@172.20.83.101 hdoop@10.40.71.115 "cd /opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_192914 && exec bash"
