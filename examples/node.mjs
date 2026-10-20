// APIFY_TOKEN=... node node.mjs [email ...]   (Node 18+, no dependencies)
const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Error: APIFY_TOKEN is not set. Get a free token at https://console.apify.com/account/integrations');
  process.exit(1);
}

const emails = process.argv.slice(2);
if (emails.length === 0) emails.push('jane@gmail.com', 'info@example.com', 'bob@mailinator.com', 'x@gmial.com', 'not-an-email');

const res = await fetch(
  `https://api.apify.com/v2/acts/pennydata~bulk-email-validator-no-smtp/run-sync-get-dataset-items?token=${encodeURIComponent(token)}`,
  { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ emails }) },
);
if (!res.ok) {
  console.error(`Error: Apify API returned ${res.status}: ${await res.text()}`);
  process.exit(1);
}
for (const r of await res.json()) {
  console.log(`${r.email ?? r.input}\t${r.status}\t${r.reason ?? ''}${r.didYouMean ? `\tdid you mean ${r.didYouMean}?` : ''}`);
}
