import requests
import psycopg2

FHIR_BASE_URL = "https://r4.smarthealthit.org"

conn = psycopg2.connect(
    dbname="fhir_integration",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

url = f"{FHIR_BASE_URL}/Patient?_count=20"

headers = {
    "Accept": "application/fhir+json"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

data = response.json()

for entry in data.get("entry", []):
    patient = entry["resource"]

    first_name = None
    last_name = None
    gender = patient.get("gender")
    birth_date = patient.get("birthDate")

    if "name" in patient:
        name = patient["name"][0]
        last_name = name.get("family")

        if "given" in name:
            first_name = name["given"][0]

    cursor.execute(
        """
        INSERT INTO patients (first_name, last_name, gender, birth_date)
        VALUES (%s, %s, %s, %s)
        """,
        (first_name, last_name, gender, birth_date)
    )

conn.commit()

print("Patients inserted successfully")

# Pull observations
obs_url = f"{FHIR_BASE_URL}/Observation?_count=100"

response = requests.get(obs_url, headers=headers)

data = response.json()

for entry in data.get("entry", []):
    obs = entry["resource"]

    patient_ref = obs.get("subject", {}).get("reference", "")
    patient_id = patient_ref.replace("Patient/", "")

    code_data = obs.get("code", {}).get("coding", [{}])[0]
    loinc_code = code_data.get("code")
    test_name = code_data.get("display")

    value = None
    unit = None

    if "valueQuantity" in obs:
        value = obs["valueQuantity"].get("value")
        unit = obs["valueQuantity"].get("unit")

    observation_date = obs.get("effectiveDateTime")

    cursor.execute(
        """
        INSERT INTO observations
        (patient_id, loinc_code, test_name, value, unit, observation_date)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (patient_id, loinc_code, test_name, value, unit, observation_date)
    )

conn.commit()

print("Observations inserted")

cursor.close()
conn.close()
