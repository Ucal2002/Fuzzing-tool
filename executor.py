import requests
import json

# Feste relevante Codes für Pentesting
RELEVANT_STATUS_CODES = {200, 400, 401, 404, 409, 500, 503, 301, 302, 307}

def send_request(payload, config, status=False):

    # Request-Daten vorbereiten
    req_data = {}
    for param, value in config["params"].items():
        req_data[param] = payload if value == "__FUZZ__" else value

    try:
        # HTTP-POST senden
        resp = requests.post(config["url"], data=req_data)

        # Immer ausgeben bei relevanten Codes, oder bei vollstendigen Statusausgaben
        if resp.status_code in RELEVANT_STATUS_CODES or status:
            print(f"[→] {resp.status_code} | {config['url']} | Payload: {payload}")

        return resp

    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
        return e 