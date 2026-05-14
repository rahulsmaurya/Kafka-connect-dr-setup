
import requests
import json
import os
from pathlib import Path

DR_CONNECT_URL = os.getenv(
    "DR_CONNECT_URL",
    "http://dr-connect:8083"
)

CONNECTOR_DIR = "/tmp/connectors"

def connector_exists(name):
    response = requests.get(
        f"{DR_CONNECT_URL}/connectors/{name}"
    )

    return response.status_code == 200

def create_connector(name, config):

    payload = {
        "name": name,
        "config": config
    }

    response = requests.post(
        f"{DR_CONNECT_URL}/connectors",
        json=payload
    )

    response.raise_for_status()

    print(f"Created connector: {name}")

def update_connector(name, config):

    response = requests.put(
        f"{DR_CONNECT_URL}/connectors/{name}/config",
        json=config
    )

    response.raise_for_status()

    print(f"Updated connector: {name}")

def deploy_connectors():

    connector_files = Path(CONNECTOR_DIR).glob("*.json")

    for file in connector_files:

        connector_name = file.stem

        with open(file) as f:
            config = json.load(f)

        try:

            if connector_exists(connector_name):
                update_connector(connector_name, config)
            else:
                create_connector(connector_name, config)

        except Exception as e:
            print(f"Failed connector {connector_name}: {e}")

if __name__ == "__main__":
    deploy_connectors()
