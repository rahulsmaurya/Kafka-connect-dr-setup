
import requests
import json
import os

PRIMARY_CONNECT_URL = os.getenv(
    "PRIMARY_CONNECT_URL",
    "http://primary-connect:8083"
)

OUTPUT_DIR = "/tmp/connectors"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_connectors():
    response = requests.get(f"{PRIMARY_CONNECT_URL}/connectors")
    response.raise_for_status()
    return response.json()

def get_connector_config(name):
    response = requests.get(
        f"{PRIMARY_CONNECT_URL}/connectors/{name}/config"
    )
    response.raise_for_status()
    return response.json()

def export_all_connectors():
    connectors = get_connectors()

    for connector in connectors:
        config = get_connector_config(connector)

        output_file = f"{OUTPUT_DIR}/{connector}.json"

        with open(output_file, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Exported connector: {connector}")

if __name__ == "__main__":
    export_all_connectors()
