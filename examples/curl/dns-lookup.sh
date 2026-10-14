#!/usr/bin/env sh
# Live DNS lookup for every record type.
# Usage: WHOISFREAKS_API_KEY=your_key ./dns-lookup.sh example.com
DOMAIN="${1:-whoisfreaks.com}"
curl -s "https://api.whoisfreaks.com/v2.0/dns/live?domainName=${DOMAIN}&type=all&apiKey=${WHOISFREAKS_API_KEY}"
