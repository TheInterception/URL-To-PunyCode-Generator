import idna
import itertools
import random

HOMOGLYPHS = {
    "a": ["a", "\u0430"],
    "c": ["c", "\u0441"],
    "e": ["e", "\u0435"],
    "i": ["i", "\u0456"],
    "o": ["o", "\u03BF"],
    "d": ["d", "\u0501"],
    "l": ["l", "\u217C"],
    "n": ["n", "\u0578"],
}

def all_variants(domain):
    name, *rest = domain.split(".")
    tld = ".".join(rest) if rest else ""
    per_char_options = [HOMOGLYPHS.get(ch, [ch]) for ch in name]
    combos = (''.join(p) for p in itertools.product(*per_char_options))

    results = []
    for combo in combos:
        full = f"{combo}.{tld}" if tld else combo
        try:
            puny = idna.encode(full).decode("ascii")
            results.append((combo, puny))
        except Exception:
            continue

    seen = set()
    unique = []
    for u, p in results:
        if p not in seen:
            seen.add(p)
            unique.append((u, p))

    return unique

def sample_variants(domain, count=10, shuffle=True):
    variants = all_variants(domain)
    total = len(variants)
    if shuffle:
        random.shuffle(variants)
    return variants[:min(count, total)], total

if __name__ == "__main__":
    domain = input("Enter domain (e.g., microsoft.com): ").strip()
    count = int(input("How many variants? ").strip())
    variants, total_available = sample_variants(domain, count)
    print(f"Total possible variants with current map: {total_available}")
    for u, p in variants:
        print(f"{u}  -->  {p}")