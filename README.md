# DNS Lookup API: Live, Historical and Reverse DNS Records in Python

Get the DNS records of any domain from Python with the [WhoisFreaks DNS Lookup API](https://whoisfreaks.com/products/dns-checker-api): A, AAAA, MX, NS, CNAME, SOA, TXT and SPF, one record type at a time or all of them in one request. The same API key gives you historical DNS (how a domain's records changed over time), reverse DNS (which domains point to an IP address or mail server) and bulk DNS lookups.

This page uses the official [Python SDK](https://github.com/WhoisFreaks/whoisfreaks-python).

A live DNS lookup for `whoisfreaks.com` with `type=all` returns the response below. It has 16 records; one of each type is shown, each with every field the API returns for that type.

```json
{
  "status": true,
  "queryTime": "2026-10-13 11:56:27",
  "domainName": "whoisfreaks.com",
  "domainRegistered": true,
  "dnsTypes": {
    "A": 1,
    "NS": 2,
    "SOA": 6,
    "MX": 15,
    "TXT": 16,
    "AAAA": 28,
    "SPF": 99
  },
  "dnsRecords": [
    {
      "name": "whoisfreaks.com",
      "type": 1,
      "dnsType": "A",
      "ttl": 300,
      "rawText": "whoisfreaks.com.\t300\tIN\tA\t188.114.96.0",
      "rRsetType": 1,
      "address": "188.114.96.0"
    },
    {
      "name": "whoisfreaks.com",
      "type": 2,
      "dnsType": "NS",
      "ttl": 21600,
      "rawText": "whoisfreaks.com.\t21600\tIN\tNS\talbert.ns.cloudflare.com.",
      "rRsetType": 2,
      "singleName": "albert.ns.cloudflare.com."
    },
    {
      "name": "whoisfreaks.com",
      "type": 6,
      "dnsType": "SOA",
      "ttl": 1800,
      "rawText": "whoisfreaks.com.\t1800\tIN\tSOA\talbert.ns.cloudflare.com. dns.cloudflare.com. 2417065744 10000 2400 604800 1800",
      "rRsetType": 6,
      "admin": "dns.cloudflare.com.",
      "host": "albert.ns.cloudflare.com.",
      "expire": 604800,
      "minimum": 1800,
      "refresh": 10000,
      "retry": 2400,
      "serial": 2417065744
    },
    {
      "name": "whoisfreaks.com",
      "type": 15,
      "dnsType": "MX",
      "ttl": 300,
      "rawText": "whoisfreaks.com.\t300\tIN\tMX\t0 whoisfreaks-com.mail.protection.outlook.com.",
      "rRsetType": 15,
      "target": "whoisfreaks-com.mail.protection.outlook.com.",
      "priority": 0
    },
    {
      "name": "whoisfreaks.com",
      "type": 16,
      "dnsType": "TXT",
      "ttl": 300,
      "rawText": "whoisfreaks.com.\t300\tIN\tTXT\t\"google-site-verification=s0lTTBfSePwOO7LWlSND2ulZUfz7h-BE15H2llWem2A\"",
      "rRsetType": 16,
      "strings": [
        "google-site-verification=s0lTTBfSePwOO7LWlSND2ulZUfz7h-BE15H2llWem2A"
      ]
    },
    {
      "name": "whoisfreaks.com",
      "type": 28,
      "dnsType": "AAAA",
      "ttl": 300,
      "rawText": "whoisfreaks.com.\t300\tIN\tAAAA\t2a06:98c1:3120:0:0:0:0:0",
      "rRsetType": 28,
      "address": "2a06:98c1:3120:0:0:0:0:0"
    },
    {
      "name": "whoisfreaks.com",
      "type": 99,
      "dnsType": "SPF",
      "ttl": 300,
      "rawText": "whoisfreaks.com.\t300\tIN\tSPF\t\"v=spf1 include:spf.protection.outlook.com include:_spf.whoisfreaks_com._d.easydmarc.pro -all\"",
      "rRsetType": 99,
      "strings": [
        "v=spf1 include:spf.protection.outlook.com include:_spf.whoisfreaks_com._d.easydmarc.pro -all"
      ]
    }
  ]
}
```

## Contents

- [Quick start](#quick-start)
- [Live DNS lookup](#live-dns-lookup)
- [What the response contains](#what-the-response-contains)
- [Historical DNS lookup](#historical-dns-lookup)
- [Reverse DNS lookup](#reverse-dns-lookup)
- [Bulk DNS lookup](#bulk-dns-lookup)
- [Use cases](#use-cases)
- [Errors and rate limits](#errors-and-rate-limits)
- [Credits](#credits)
- [FAQ](#faq)
- [Other languages and related APIs](#other-languages-and-related-apis)

## Quick start

**1. Install the SDK** (Python 3.8 or later):

```sh
pip install "whoisfreaks>=0.23.0"
```

**2. Get an API key.** Create a free account at [billing.whoisfreaks.com/signup](https://billing.whoisfreaks.com/signup). New accounts get 500 free credits with no credit card.

**3. Keep the key out of your code.** Export it as an environment variable:

```sh
export WHOISFREAKS_API_KEY="your_api_key"
```

**4. Configure the client once.** Every example below starts from this setup:

```python
import os
import whoisfreaks

config = whoisfreaks.Configuration()
config.api_key["ApiKeyAuth"] = os.environ["WHOISFREAKS_API_KEY"]
```

## Live DNS lookup

A live lookup queries DNS when you call it and returns every matching record. Pass `"all"` for every record type, or a comma-separated list such as `"A,MX,TXT"`.

```python
with whoisfreaks.ApiClient(config) as client:
    dns = whoisfreaks.DNSApi(client)
    result = dns.dns_live("A,MX,TXT", domain_name="whoisfreaks.com")

    print(result.domain_name, result.query_time)
    for record in result.dns_records or []:
        print(record.dns_type, record.ttl, record.raw_text)
```

The same request over plain HTTP:

```sh
curl "https://api.whoisfreaks.com/v2.0/dns/live?domainName=whoisfreaks.com&type=A,MX,TXT&apiKey=$WHOISFREAKS_API_KEY"
```

To get the PTR record of an IP address, pass `ip_address` instead of, or as well as, `domain_name`:

```python
with whoisfreaks.ApiClient(config) as client:
    result = whoisfreaks.DNSApi(client).dns_live("all", ip_address="8.8.8.8")

    for record in result.dns_records or []:
        print(record.single_name)   # dns.google.
```

<details>
<summary>Example response for 8.8.8.8</summary>

```json
{
  "status": true,
  "queryTime": "2026-10-13 11:56:28",
  "ipAddress": "8.8.8.8",
  "dnsTypes": {
    "PTR": 12
  },
  "dnsRecords": [
    {
      "name": "8.8.8.8.in-addr.arpa",
      "type": 12,
      "dnsType": "PTR",
      "ttl": 12537,
      "rawText": "8.8.8.8.in-addr.arpa.\t12537\tIN\tPTR\tdns.google.",
      "rRsetType": 12,
      "singleName": "dns.google."
    }
  ]
}
```

</details>

## What the response contains

| Field | What it holds |
|---|---|
| `status` | Whether the lookup succeeded |
| `queryTime` | When the lookup ran |
| `domainName` or `ipAddress` | What was looked up |
| `domainRegistered` | Whether the domain is registered |
| `dnsTypes` | Each record type in the response mapped to its numeric DNS type code, for example `"MX": 15` |
| `dnsRecords` | The records, each with `name`, `type` (numeric), `dnsType` (name), `ttl`, `rawText` (zone-file line), `rRsetType` and the fields for its type below |

| Type | What it holds | Fields | Typical use |
|---|---|---|---|
| `A` | IPv4 address | `address` | Find where a site is hosted |
| `AAAA` | IPv6 address | `address` | Check IPv6 support |
| `MX` | Mail server and its priority | `target`, `priority` | Find the email provider |
| `NS` | Authoritative name server | `singleName` | Find the DNS provider |
| `CNAME` | Canonical name (alias) | `singleName` | Follow a subdomain to its target |
| `PTR` | Host name for an IP address | `singleName` | Reverse-resolve an IP |
| `SOA` | Zone authority and timers | `host`, `admin`, `serial`, `refresh`, `retry`, `expire`, `minimum` | Spot zone changes |
| `TXT` | Free-form text, including verification tokens | `strings` | See which services a domain uses |
| `SPF` | Allowed mail senders | `strings` | Check email authentication |

## Historical DNS lookup

The historical DNS API returns the DNS snapshots recorded for a domain over time, from a database of billions of records. Use it to see when a domain moved hosts, switched email providers or changed name servers.

```python
with whoisfreaks.ApiClient(config) as client:
    history = whoisfreaks.DNSApi(client).dns_historical("whoisfreaks.com", "all", page=1)

    print(history.total_records, "snapshots on", history.total_pages, "pages")
    for snapshot in history.historical_dns_records or []:
        print(snapshot.query_time, len(snapshot.dns_records or []), "records")
```

Each snapshot has the same shape as a live lookup. When `totalPages` is more than 1, pass `page=2` and so on for the rest. Each page costs 2 credits.

<details>
<summary>Example response: page 1 of whoisfreaks.com's 109 snapshots (2 pages); one snapshot is shown, with one record of each type</summary>

```json
{
  "totalRecords": 109,
  "totalPages": 2,
  "currentPage": 1,
  "historicalDnsRecords": [
    {
      "queryTime": "2023-02-24",
      "domainName": "whoisfreaks.com.",
      "dnsTypes": {
        "A": 1,
        "SPF": 99
      },
      "dnsRecords": [
        {
          "name": "whoisfreaks.com",
          "type": 1,
          "dnsType": "A",
          "ttl": 3600,
          "rawText": "whoisfreaks.com.\t3600\tIN\tA\t45.79.216.218",
          "rRsetType": 1,
          "address": "45.79.216.218"
        },
        {
          "name": "whoisfreaks.com",
          "type": 99,
          "dnsType": "SPF",
          "ttl": 3600,
          "rawText": "whoisfreaks.com.\t3600\tIN\tSPF\t\"v=spf1 include:zoho.com ~all\"",
          "rRsetType": 99,
          "strings": [
            "v=spf1 include:zoho.com ~all"
          ]
        }
      ]
    }
  ]
}
```

</details>

## Reverse DNS lookup

Reverse DNS works backward from a value to the domains that use it. Search an IPv4 or IPv6 address (or CIDR range) in A and AAAA records, or a mail server, name server or other value in MX, NS, CNAME, TXT, SPF and SOA records.

```python
with whoisfreaks.ApiClient(config) as client:
    matches = whoisfreaks.DNSApi(client).dns_reverse("8.8.8.8", "a", page=1)

    print(matches.total_records, "domains on", matches.total_pages, "pages")
    for match in matches.reverse_dns_records or []:
        print(match.domain_name)
```

For record types other than A and AAAA, set `exact=False` to match with a `*` wildcard, for example every domain whose MX record ends in `.google.com`. Each page returns up to 100 records and costs 5 credits.

<details>
<summary>Example response: 101,168 domains point to 8.8.8.8; two of the 100 on page 1 are shown</summary>

```json
{
  "totalRecords": 101168,
  "totalPages": 1012,
  "currentPage": 1,
  "reverseDnsRecords": [
    {
      "queryTime": "2026-08-13",
      "domainName": "invisible.ac.nz",
      "dnsTypes": {
        "A": 1
      },
      "dnsRecords": [
        {
          "name": "invisible.ac.nz",
          "type": 1,
          "dnsType": "A",
          "ttl": 3600,
          "rawText": "invisible.ac.nz.\t3600\tIN\tA\t8.8.8.8",
          "rRsetType": 1,
          "address": "8.8.8.8"
        }
      ]
    },
    {
      "queryTime": "2026-08-03",
      "domainName": "pucal.de",
      "dnsTypes": {
        "A": 1
      },
      "dnsRecords": [
        {
          "name": "pucal.de",
          "type": 1,
          "dnsType": "A",
          "ttl": 21600,
          "rawText": "pucal.de.\t\t21600\tIN\tA\t8.8.8.8",
          "rRsetType": 1,
          "address": "8.8.8.8"
        }
      ]
    }
  ]
}
```

</details>

## Bulk DNS lookup

Look up many domains in one request:

```python
with whoisfreaks.ApiClient(config) as client:
    request = whoisfreaks.DnsBulkRequest(domain_names=["whoisfreaks.com", "example.com"])
    result = whoisfreaks.DNSApi(client).dns_bulk("A,MX", request)

    for item in result.bulk_dns_info or []:
        print(item.domain_name, len(item.dns_records or []))
```

You pay 1 credit per domain that returns records.

<details>
<summary>Example response</summary>

```json
{
  "bulk_dns_info": [
    {
      "status": true,
      "queryTime": "2026-10-13 11:56:53",
      "domainName": "whoisfreaks.com",
      "domainRegistered": true,
      "dnsTypes": {
        "MX": 15,
        "A": 1
      },
      "dnsRecords": [
        {
          "name": "whoisfreaks.com",
          "type": 1,
          "dnsType": "A",
          "ttl": 300,
          "rawText": "whoisfreaks.com.\t300\tIN\tA\t188.114.96.2",
          "rRsetType": 1,
          "address": "188.114.96.2"
        },
        {
          "name": "whoisfreaks.com",
          "type": 1,
          "dnsType": "A",
          "ttl": 300,
          "rawText": "whoisfreaks.com.\t300\tIN\tA\t188.114.97.2",
          "rRsetType": 1,
          "address": "188.114.97.2"
        },
        {
          "name": "whoisfreaks.com",
          "type": 15,
          "dnsType": "MX",
          "ttl": 300,
          "rawText": "whoisfreaks.com.\t300\tIN\tMX\t0 whoisfreaks-com.mail.protection.outlook.com.",
          "rRsetType": 15,
          "target": "whoisfreaks-com.mail.protection.outlook.com.",
          "priority": 0
        }
      ]
    },
    {
      "status": true,
      "queryTime": "2026-10-13 11:56:53",
      "domainName": "example.com",
      "domainRegistered": true,
      "dnsTypes": {
        "MX": 15,
        "A": 1
      },
      "dnsRecords": [
        {
          "name": "example.com",
          "type": 1,
          "dnsType": "A",
          "ttl": 300,
          "rawText": "example.com.\t\t300\tIN\tA\t104.20.23.154",
          "rRsetType": 1,
          "address": "104.20.23.154"
        },
        {
          "name": "example.com",
          "type": 1,
          "dnsType": "A",
          "ttl": 300,
          "rawText": "example.com.\t\t300\tIN\tA\t172.66.147.243",
          "rRsetType": 1,
          "address": "172.66.147.243"
        },
        {
          "name": "example.com",
          "type": 15,
          "dnsType": "MX",
          "ttl": 59,
          "rawText": "example.com.\t\t59\tIN\tMX\t0 .",
          "rRsetType": 15,
          "target": ".",
          "priority": 0
        }
      ]
    }
  ]
}
```

</details>

## Use cases

**Email deliverability checks.** Pull `MX`, `SPF` and `TXT` records to see which provider handles a domain's mail and whether its sender policy is set up.

**Infrastructure mapping.** Run a reverse DNS lookup on an IP address or mail server to find every other domain that shares it. Security teams use this to expand from one suspicious domain to the rest of a campaign.

**Change tracking.** Compare historical DNS snapshots to find when a domain changed hosting, email or DNS provider, and confirm the timing of a migration or an incident.

**Portfolio audits.** Run a bulk lookup over every domain you own and flag the ones that point at an old server or are missing mail records:

```python
domains = ["whoisfreaks.com", "example.com"]

with whoisfreaks.ApiClient(config) as client:
    result = whoisfreaks.DNSApi(client).dns_bulk(
        "MX", whoisfreaks.DnsBulkRequest(domain_names=domains)
    )

no_mail = [item.domain_name for item in result.bulk_dns_info or [] if not item.dns_records]
print("No MX records:", no_mail)
```

## Errors and rate limits

Failed requests raise `ApiException` with the HTTP status code and the response body:

```python
from whoisfreaks.rest import ApiException

with whoisfreaks.ApiClient(config) as client:
    try:
        result = whoisfreaks.DNSApi(client).dns_live("all", domain_name="whoisfreaks.com")
    except ApiException as e:
        print(e.status, e.body)
```

| Status | Meaning |
|---|---|
| 401 | Missing, invalid or suspended API key |
| 429 | Rate limit reached for this minute |

Rate limits are counted per minute, per endpoint category, and depend on your plan. A request that is throttled does not use a credit. Every response carries `x-ratelimit-allowed-requests`, `x-ratelimit-remaining-requests` and `x-ratelimit-remaining-time` (time until the window resets, in nanoseconds). The `_with_http_info` variant of each method returns these headers:

```python
with whoisfreaks.ApiClient(config) as client:
    response = whoisfreaks.DNSApi(client).dns_live_with_http_info("all", domain_name="whoisfreaks.com")

    print(response.headers.get("x-ratelimit-remaining-requests"))
    result = response.data
```

On a 429, wait until `x-ratelimit-remaining-time` has passed, plus a small buffer, then retry. See [API rate limiting](https://whoisfreaks.com/documentation/api-rate-limiting).

## Credits

| Request | Credits |
|---|---|
| Live DNS | 1 per domain |
| Bulk DNS | 1 per domain that returns records |
| Historical DNS | 2 per page |
| Reverse DNS | 5 per page (up to 100 records) |

Full pricing: [credit usage](https://whoisfreaks.com/documentation/credit-usage).

## FAQ

**Is there a free DNS lookup API?**
Yes. A free WhoisFreaks account includes 500 credits with no credit card, which covers 500 live DNS lookups.

**Can I get every record type in one call?**
Yes. Pass `"all"` as the record type.

**Does the API do reverse IP lookups?**
Yes, two kinds. A live lookup with `ip_address` returns the PTR record for that IP. A reverse DNS lookup returns the domains whose A or AAAA records point to it.

**Can I get XML instead of JSON?**
Yes. Pass `format="xml"` in Python or `&format=xml` over HTTP.

## Other languages and related APIs

The DNS Lookup API has official SDKs for [Python](https://github.com/WhoisFreaks/whoisfreaks-python), [JavaScript](https://github.com/WhoisFreaks/whoisfreaks-javascript), [TypeScript](https://github.com/WhoisFreaks/whoisfreaks-typescript), [Java](https://github.com/WhoisFreaks/whoisfreaks-java), [Kotlin](https://github.com/WhoisFreaks/whoisfreaks-kotlin), [Go](https://github.com/WhoisFreaks/whoisfreaks-go), [C#](https://github.com/WhoisFreaks/whoisfreaks-csharp), [Ruby](https://github.com/WhoisFreaks/whoisfreaks-ruby), [PHP](https://github.com/WhoisFreaks/whoisfreaks-php) and [Swift](https://github.com/WhoisFreaks/whoisfreaks-swift).

Related quick starts with the same API key:

- [WHOIS API](https://github.com/WhoisFreaks/whois-api): live, historical, reverse and bulk WHOIS
- [Domain availability API](https://github.com/WhoisFreaks/domain-availability-api): check if a domain is available and get suggestions on other TLDs

Documentation: [DNS lookup API](https://whoisfreaks.com/documentation/dns-checker-api). Questions: support@whoisfreaks.com.
