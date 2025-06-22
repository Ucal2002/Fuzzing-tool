import re

# Liste bekannter Fehler-Muster
ERROR_PATTERNS = [
    r"SQL syntax.*MySQL", 
    r"Warning.*mysql_", 
    r"Unclosed quotation mark after the character string", 
    r"quoted string not properly terminated", 
    r"Microsoft OLE DB Provider for ODBC Drivers", 
    r"ORA-\d+",  # Oracle
    r"PostgreSQL.*ERROR", 
    r"PG::SyntaxError", 
    r"Stack trace", 
    r"Exception.* at ", 
    r"System\.Web\.HttpUnhandledException", 
    r"InvalidArgumentException", 
    r"Undefined variable", 
    r"Undefined index", 
    r"Fatal error", 
    r"Parse error", 
    r"Internal Server Error", 
    r"you have an error in your sql syntax",
    r"unexpected token",
    r"TypeError",
    r"ReferenceError",
    r"Segmentation fault",
]

def analyze(response, payload):
    """
    Analysiert die HTTP-Response.
    Gibt True zurück, wenn verdächtige Fehlermuster gefunden werden.
    """

    if not response:
        return False 

    body = response.text

    # Alle Patterns durchlaufen
    for pattern in ERROR_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            print(f"[!] Possible vuln detected: pattern '{pattern}' in response!")
            return True

    return False