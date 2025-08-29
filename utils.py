import re

PHONE_RE = re.compile(r'^[0-9+]{8,20}$')

def is_valid_phone(s: str) -> bool:
    return bool(PHONE_RE.fullmatch(s or ""))

def normalize_phone(s: str) -> str:
    s = (s or "").strip().replace(" ", "").replace("-", "")
    # Ensure starts with 0 or +; this is simplistic and just for demo
    if not s:
        return s
    if s[0] not in "+0":
        s = "0" + s
    return s