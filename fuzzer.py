import json
from mutator import mutate
from mutator import mutatev2
from executor import send_request
from analyzer import analyze
from logger import log

print(""" @@@@@@@@ @@@  @@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@ 
 @@!      @@!  @@@      @@!      @@! @@!      @@!  @@@
 @!!!:!   @!@  !@!    @!!      @!!   @!!!:!   @!@!!@! 
 !!:      !!:  !!!  !!:      !!:     !!:      !!: :!! 
  :        :.:: :  :.::.: : :.::.: : : :: :::  :   : :
                                                      """)
def menu1():
    print("Please enter your Fuzzing configuration by choosing a number:")
    print("[1]Random mutation")
    print("[2]Systemetec Mutation")
    mode = input("Enter here: ")

print("\nPlease enter your mutuatuion kategory by choosing a number:")
print("[1] Alle Kategorien")
print("[2] SQLi")
print("[3] XSS")
print("[4] Traversal")
print("[5] Format Strings")
category_imput = input("Deine Wahl: ").strip()

category_map = {
    "1": "ALL",
    "2": "SQLi",
    "3": "XSS",
    "4": "Traversal",
    "5": "Format"
}

selected_category = category_map.get(category_imput, "ALL")
print(f"\n→ Modus: {mode}, Kategorie: {selected_category}\n")

with open("config.json") as f:
    config = json.load(f)

with open(config["seeds_file"]) as f:
    seeds = [line.strip() for line in f]

match mode:
    case "1":  # Zufällig
        for seed in seeds:
            payload = mutate(seed)
            response = send_request(payload, config)
            if analyze(response, payload):
                log(payload, response, None)
    case "2":  # Systematisch
        for seed in seeds:
                    for category, payload in mutatev2(seed, category):
                        print(f"[+] Systematisch ({category}): {payload}")
                        response = send_request(payload, config)
                        print(f"    Status: {response.status_code}")
                        if analyze(response, payload):
                            log(payload, response, category)
    case _:
            print("Ungültiger Modus.")
        


for seed in seeds:
    for category, payload in mutatev2(seed):
        print(f"[+] Testing ({category}): {payload}")
        response = send_request(payload, config)
        print(f"    Status: {response.status_code}")

        if analyze(response, payload):
            log(payload, response, category)

    print(f"[+] Fuzzing with payload: {payload}")
    print(f"    Status: {response.status_code}")
    print(f"    Body: {response.text[:100]}")
