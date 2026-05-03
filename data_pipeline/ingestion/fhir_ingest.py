import json
import requests
import os

FHIR_SERVER = "http://localhost:8080/fhir"
DATA_FOLDER = "fhir"

headers = {
    "Content-Type": "application/fhir+json"
}

def upload_bundle(bundle):
    url = FHIR_SERVER
    response = requests.post(url, headers=headers, json=bundle)
    return response.status_code, response.text

def process_bundle(file_path):
    with open(file_path, "r") as f:
        bundle = json.load(f)

    status, response_text = upload_bundle(bundle)
    print(f"Bundle upload → {status}")

def main():
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(DATA_FOLDER, filename)
            print(f"\nProcessing {filename}")
            process_bundle(file_path)

if __name__ == "__main__":
    main()
