import json
from mutator import mutate
from executor import send_request
from analyzer import analyze
from logger import log

print(""" @@@@@@@@ @@@  @@@ @@@@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@ 
 @@!      @@!  @@@      @@!      @@! @@!      @@!  @@@
 @!!!:!   @!@  !@!    @!!      @!!   @!!!:!   @!@!!@! 
 !!:      !!:  !!!  !!:      !!:     !!:      !!: :!! 
  :        :.:: :  :.::.: : :.::.: : : :: :::  :   : :
                                                      """)
print("Please enter your Fuzzing configuration:")
input("\n[↩]  press Enter, to start fuzzing from the default configuration file...")


with open("config.json") as f:
    config = json.load(f)

with open(config["seeds_file"]) as f:
    seeds = [line.strip() for line in f]

for seed in seeds:
    payload = mutate(seed)
    response = send_request(payload, config)
    if analyze(response, payload):
        log(payload, response)


    print(f"[+] Fuzzing with payload: {payload}")
    print(f"    Status: {response.status_code}")
    print(f"    Body: {response.text[:100]}")
