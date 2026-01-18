#!/bin/bash


if [ "$1" = "--vpn" ]; then
   
    cd /vpn-eti/vpn2023/
    sudo openvpn --config vpnWETI.ovpn --auth-user-pass vpnWETI.user --daemon
fi


ssh -L 19290:student-swarm01.maas:19290 rsww@172.20.83.101