#!/bin/bash
#Script to process ip ranges to ban using IPSet and IPTables
ipset create countryblock hash:net
while read line; do ipset add countryblock $line; done < whitelist.txt
iptables-legacy -I INPUT -m set --match-set countryblock src -j ACCEPT
iptables-legacy -A INPUT -p tcp --dport 8000 -j DROP
