import csv
import os

LOG_FILE = "fuzz_results.csv"

# CSV Header definieren (nur beim ersten Mal schreiben)
CSV_HEADER = ["Payload", "Category", "StatusCode", "Snippet"]

def log(payload, response, category):
    """
    Loggt gefundene Fehler in fuzz_results.csv.
    Speichert: Payload, Kategorie, HTTP-Code, Response-Ausschnitt.
    """

    if not response:
        return

    # Prüfen ob Datei existiert → Header schreiben wenn neu
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(CSV_HEADER)

        snippet = response.text[:100].replace('\n', ' ').replace('\r', ' ')

        writer.writerow([payload, category, response.status_code, snippet])

    print(f"[LOG] Saved to {LOG_FILE}: {payload} ({response.status_code})")