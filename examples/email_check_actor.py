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
