# pip install requests
# APIFY_TOKEN=... python python_example.py [email ...]
import os
import sys

import requests

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Error: APIFY_TOKEN is not set. Get a free token at https://console.apify.com/account/integrations")

emails = sys.argv[1:] or ["jane@gmail.com", "info@example.com", "bob@mailinator.com", "x@gmial.com", "not-an-email"]

resp = requests.post(
    "https://api.apify.com/v2/acts/pennydata~bulk-email-validator-no-smtp/run-sync-get-dataset-items",
    params={"token": token},
    json={"emails": emails},
    timeout=300,
)
if not resp.ok:
    sys.exit(f"Error: Apify API returned {resp.status_code}: {resp.text[:300]}")
for r in resp.json():
    print(r.get("email") or r.get("input"), r.get("status"), r.get("reason") or "", r.get("didYouMean") or "", sep="\t")
