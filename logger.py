def log(payload, response, category):
    with open("crashes.log", "a") as f:
        f.write(f"Category: {category}\n")
        f.write(f"Payload: {payload}\n")
        f.write(f"Status: {response.status_code}\n")
        f.write(f"Response: {response.text[:200]}\n\n")
