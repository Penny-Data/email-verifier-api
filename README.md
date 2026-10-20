# Bulk Email Verifier API (no SMTP): validate an email list by syntax, MX and disposable check

A **bulk email verifier API** that cleans an email list **without SMTP probing**. For every address it checks syntax, domain DNS/MX records, disposable (throwaway) domains, role accounts (`info@`, `admin@`), free providers (Gmail, Yahoo...) and common typos (`gmial.com` -> `gmail.com`). Pay per checked email, DNS failures are not billed.

It runs as the [`pennydata/bulk-email-validator-no-smtp`](https://apify.com/pennydata/bulk-email-validator-no-smtp) Actor on Apify, so you call it over plain HTTP, with an Apify client, or from the Console with no code.

**Actor page:** https://apify.com/pennydata/bulk-email-validator-no-smtp

## What "no SMTP" means (read this)

This tool **never connects to the recipient's mail server**. It does an **email syntax, MX and disposable check** only. So it can tell you an address is malformed, its domain cannot receive mail, or it is a disposable/role address. It **cannot confirm that a specific mailbox exists** and does not claim to. If you need mailbox-level verification, you need an SMTP-probing service.

## Pricing

Pay per event, no subscription. Read from the live actor page on 2026-10-20:

| Event | Price |
| --- | --- |
| Email validated | $0.0008 each (**$0.80 per 1,000**) |

Rows with unknown DNS status are not charged. Prices can change and paid Apify plans may get lower per-event prices; the [actor page](https://apify.com/pennydata/bulk-email-validator-no-smtp) is the source of truth. A new Apify account includes free monthly platform credit.

## Quick start

Get an API token at https://console.apify.com/account/integrations and export it:

```bash
export APIFY_TOKEN=your_token_here
```

### curl: validate an email list

```bash
curl -X POST "https://api.apify.com/v2/acts/pennydata~bulk-email-validator-no-smtp/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"emails":["jane@gmail.com","info@example.com","bob@mailinator.com","x@gmial.com","not-an-email"]}'
```

Each response item looks like (illustrative shape, from the Actor's documented output):

```json
{
  "input": "bob@mailinator.com",
  "email": "bob@mailinator.com",
  "valid": false,
  "status": "disposable",
  "reason": "disposable_domain",
  "domain": "mailinator.com",
  "hasMx": true,
  "isDisposable": true,
  "isRole": false,
  "isFreeProvider": false,
  "didYouMean": null
}
```

### Node.js (no dependencies, Node 18+)

```bash
APIFY_TOKEN=... node examples/node.mjs jane@gmail.com bob@mailinator.com
```

### Python

```bash
pip install requests
APIFY_TOKEN=... python examples/python_example.py jane@gmail.com bob@mailinator.com
```

### From a CSV

Set `csvUrl` (public http(s) CSV) and optionally `csvColumn`; see [`examples/input-csv.json`](examples/input-csv.json) and run `./examples/curl.sh examples/input-csv.json`.

Without `APIFY_TOKEN` all example scripts exit non-zero with a clear error and make no request.

## Input reference

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `emails` | string[] | | Addresses to validate |
| `csvUrl` | string | | Public URL of a CSV; uses the column whose header contains "email", or the first column |
| `csvColumn` | string | | Header of the email column |
| `maxEmails` | integer | `10000` | Safety cap on unique emails per run (max 100000) |
| `concurrency` | integer | `10` | Parallel DNS validations (1-100) |

Duplicates are removed (case-insensitive) and validated once. Full schema on the [actor page](https://apify.com/pennydata/bulk-email-validator-no-smtp/input-schema).

## Use cases

Cleaning a mailing list before a send, filtering disposable sign-ups, flagging role addresses in lead lists, catching typos in domains, pre-screening a CSV export.

## AI-built disclosure

This repository and the underlying Actor were built and are maintained by an AI-assisted workflow (Claude), operated by the owner of the `jjlarsensa` GitHub account and the `pennydata` Apify account. Run the examples yourself before depending on them.

## License

MIT, see [LICENSE](LICENSE). The Actor itself is a hosted service on Apify.
