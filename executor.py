import requests
import json
import configparser

def send_request(payload, config):
    data = {}
    for k, v in config["params"].items():
        data[k] = payload if v == "__FUZZ__" else v

    response = requests.post(config["url"], data=data)
    return response