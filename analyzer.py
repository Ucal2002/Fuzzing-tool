def analyze(response, payload):
    if response.status_code >= 500 or "Exception" in response.text:
        print(f"[!] Possible crash with payload: {payload}")
        return True
    return False
