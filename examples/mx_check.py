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
