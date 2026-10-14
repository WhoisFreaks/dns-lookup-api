"""Live DNS lookup with the WhoisFreaks Python SDK.

    pip install "whoisfreaks>=0.23.0"
    WHOISFREAKS_API_KEY=your_key python dns_lookup.py example.com A,MX,TXT
"""
import os
import sys

import whoisfreaks

domain = sys.argv[1] if len(sys.argv) > 1 else "whoisfreaks.com"
record_types = sys.argv[2] if len(sys.argv) > 2 else "all"

config = whoisfreaks.Configuration()
config.api_key["ApiKeyAuth"] = os.environ["WHOISFREAKS_API_KEY"]

with whoisfreaks.ApiClient(config) as client:
    records = whoisfreaks.DNSApi(client).dns_live(record_types, domain_name=domain)

print(records)
