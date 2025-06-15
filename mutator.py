import random

def mutate(seed):
    mutations = [
        "' OR '1'='1",
        "<script>alert(1)</script>",
        "../../../../etc/passwd",
        "A" * 500,
        "%00%00%00",
    ]
    return seed + random.choice(mutations)

def mutatev2(seed):
    """Kombiniert den Seed mit allen Mutationen aus allen Kategorien.
    Gibt Tupel (Kategorie, mutierter_payload) zurück."""

    categories = {
        "SQLi": [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' OR 1=1 --"
        ],
        "XSS": [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg><script>alert(1)</script></svg>"
        ],
        "Traversal": [
            "../../etc/passwd",
            "..\\..\\..\\..\\windows\\win.ini",
            "/../../../boot.ini"
        ],
        "Format": [
            "A" * 500,
            "%x%x%x%x",
            "\x00\x00\x00"
        ]
    }

    all_mutations = []

    for category, mutation_list in categories.items():
        for mutation in mutation_list:
            payload = seed + mutation
            all_mutations.append((category, payload))

    return all_mutations
