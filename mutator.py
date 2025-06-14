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
