import json
import time
from mutator import mutate, mutatev2, mutatev3
from executor import send_request
from analyzer import analyze
from logger import log


# ASCII Banner
print(""" 
 @@@@@@@@ @@@  @@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@ 
 @@!      @@!  @@@      @@!      @@! @@!      @@!  @@@
 @!!!:!   @!@  !@!    @!!      @!!   @!!!:!   @!@!!@! 
 !!:      !!:  !!!  !!:      !!:     !!:      !!: :!! 
  :        :.:: :  :.::.: : :.::.: : : :: :::  :   : :
                                                      """)

# Menü für Fuzzing-Modus
print("Please enter your Fuzzing configuration by choosing a number:")
print("[1] Random mutation")
print("[2] Systematic mutation")
print("[3] Mutation from File")
mode = input("Enter here: ").strip()

ayloadfile = ""
if mode == "3":
    payloadfile = input("\nPlease enter path to your Payload-File (e.g. my_payloads.txt): ").strip()

# Menü für Mutation-Kategorie
print("\nPlease enter your mutation category by choosing a number:")
print("[1] All categories")
print("[2] SQLi")
print("[3] XSS")
print("[4] Traversal")
print("[5] Format Strings")
print("[6] Lengthbased Mutations")
category_input = input("Your Choice: ").strip()

# Mapping
category_map = {
    "1": "ALL",
    "2": "SQLi",
    "3": "XSS",
    "4": "Traversal",
    "5": "Format",
    "6": "Length"
}

selected_category = category_map.get(category_input, "ALL")


# Menü für Show all Modus
print("\nDo you want to see all status codes?")
print("[1] Yes (show all status codes)")
print("[2] No  (show only relevant status codes)")
status_input = input("Your Choice: ").strip()

status_mode = True if status_input == "1" else False

# Zusammenfassung anzeigen
print(f"\n→ Mode: {mode}")
print(f"→ Category: {selected_category}")
if mode == "3":
    print(f"→ Payload-File: {payloadfile}\n")
time.sleep(3)

# Konfig laden
with open("config.json") as f:
    config = json.load(f)

with open(config["seeds_file"]) as f:
    seeds = [line.strip() for line in f]

# Main Fuzzing Loop
match mode:
    case "1":  # Random Mutation
        for seed in seeds:
            payload = mutate(seed)
            response = send_request(payload, config, status_mode)
            if(status_mode == "true"):
                print(f"[+] Random {payload}")
                print(f"    Status: {response.status_code}")
                print(f"    Body: {response.text[:100]}")

            if analyze(response, payload) or status_mode:
                log(payload, response, category)

    case "2":  # Systematic Mutation
        for seed in seeds:
            for category, payload in mutatev2(seed, selected_category):
                response = send_request(payload, config, status_mode)
                if(status_mode == "true"):
                    print(f"[+] Systematic ({category}): {payload}")
                    print(f"    Status: {response.status_code}")
                    print(f"    Body: {response.text[:100]}")

                if analyze(response, payload) or status_mode:
                    log(payload, response, category)

    case "3":  # File
           for seed in seeds:
                for category, payload in mutatev3(seed, payloadfile):
                    response = send_request(payload, config, status_mode)
                    if(status_mode == "true"):
                        print(f"[+] Payloadfile : {payload}")
                        print(f"    Status: {response.status_code}")
                        print(f"    Body: {response.text[:100]}")

                    if analyze(response, payload):
                        log(payload, response, category)

    case _:
        print("Ungültiger Modus.")