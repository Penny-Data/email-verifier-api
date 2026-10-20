# How to Check if an Email Address Exists Without Sending an Email (What You Can Actually Know)

## Three levels of "exists"

- **Syntax**: is it shaped like an address? Fully knowable offline.
- **Domain**: does the part after `@` exist and accept mail (MX records, or an A record as fallback)? Knowable with a DNS query, no email sent.
- **Mailbox**: does that specific user exist at that domain? **Not provable without contacting the mail server**, and often not even then.

Anyone selling a flat "this inbox exists" answer without sending mail is either probing SMTP (see below) or guessing. What you can do for free is rule out the addresses that cannot possibly work.

## Syntax + MX check in Python

```python
import re, sys, dns.resolver
EMAIL = re.compile(r"^[^@\s]+@([^@\s]+\.[^@\s]+)$")
def check(addr):
    m = EMAIL.match(addr)
    if not m: return "bad-syntax"
    domain = m.group(1).lower()
    try:
        dns.resolver.resolve(domain, "MX"); return "mx-ok"
    except dns.resolver.NoAnswer:
        try: dns.resolver.resolve(domain, "A"); return "a-fallback"
        except Exception: return "no-mail-host"
    except Exception: return "no-domain"
for a in sys.argv[1:]: print(a, check(a))
```

Run with `pip install dnspython` then `python mx.py a@gmail.com b@nonexistent-zzq91.com bad`. Output when tested: `mx-ok`, `no-domain`, `bad-syntax`. A domain with no MX but an A record falls back to implicit-MX behaviour per RFC 5321, hence the `a-fallback` branch.

## Disposable and role addresses

Two more offline signals. **Disposable domains** (mailinator and similar) accept mail but are throwaway: keep a set of known domains from a public, maintained list and test `domain in DISPOSABLE`. **Role addresses** (`info@`, `admin@`, `support@`) usually reach a team, not a person: test the local part against a small set. Both lists go stale, so refresh them.

```python
DISPOSABLE = {"mailinator.com", "guerrillamail.com", "10minutemail.com"}  # load a maintained list instead
ROLES = {"info", "admin", "support", "sales", "postmaster", "abuse"}

def flags(addr):
    local, _, domain = addr.lower().partition("@")
    return {"disposable": domain in DISPOSABLE, "role": local in ROLES}
```

## Why SMTP probing is unreliable

The classic trick connects to the MX host and issues `RCPT TO` to see whether the recipient is rejected. In practice:

- **Catch-all domains** accept every recipient, so every address looks valid.
- **Outbound port 25 is blocked** by most cloud providers and many ISPs.
- **Big providers** throttle, greylist or give non-committal answers to probes.
- **Reputation risk**: repeated probing from one IP can get it blocklisted, which then hurts your real mail.

Treat an SMTP "valid" as a hint, never a guarantee. The honest approach is to filter out everything provably bad (syntax, dead domains, disposable) and let real delivery or a double opt-in confirm the rest.

## Bulk: a whole list at once

Disclosure: I built an Apify actor that runs these checks (syntax, MX, disposable, role, free-provider flags, typo suggestions) on lists, [pennydata/bulk-email-validator-no-smtp](https://apify.com/pennydata/bulk-email-validator-no-smtp). It deliberately does no SMTP probing, so it does not tell you a mailbox exists. Pay-per-event: $0.0008 per email validated (read live from the actor API on 2026-10-20; check the actor page for the current price); rows with unknown DNS status are not charged.

```python
import os, sys, requests

token = os.getenv("APIFY_TOKEN")
if not token:
    sys.exit("Error: APIFY_TOKEN is not set. Get a token at https://console.apify.com/account/integrations")

resp = requests.post(
    "https://api.apify.com/v2/acts/pennydata~bulk-email-validator-no-smtp/run-sync-get-dataset-items",
    params={"token": token},
    json={"emails": ["jane@gmail.com", "info@example.com", "bob@mailinator.com", "not-an-email"]},
    timeout=300,
)
if not resp.ok:
    sys.exit(f"Error: Apify API returned {resp.status_code}: {resp.text[:300]}")
for r in resp.json():
    print(r.get("email") or r.get("input"), r.get("status"), r.get("reason") or "", sep="\t")
```

Needs `APIFY_TOKEN`; exits with an error message if it is not set.

[Hosted option: pennydata/bulk-email-validator-no-smtp on Apify](https://apify.com/pennydata/bulk-email-validator-no-smtp)

---
Written with AI (Claude). The author also built the linked Apify actor. Code examples were run on 2026-10-20; prices are read from the live actor API and may change.
