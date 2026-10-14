// Live DNS lookup with the WhoisFreaks API. Node.js 18+ (built-in fetch).
// Usage: WHOISFREAKS_API_KEY=your_key node dns-lookup.mjs example.com A,MX,TXT
const domain = process.argv[2] ?? "whoisfreaks.com";
const type = process.argv[3] ?? "all";

const url = new URL("https://api.whoisfreaks.com/v2.0/dns/live");
url.search = new URLSearchParams({
  domainName: domain,
  type,
  apiKey: process.env.WHOISFREAKS_API_KEY,
});

const res = await fetch(url);
if (!res.ok) {
  console.error(res.status, await res.text());
  process.exit(1);
}
console.log(JSON.stringify(await res.json(), null, 2));
