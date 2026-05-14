
import requests
import os

DR_CONNECT_URL = os.getenv(
    "DR_CONNECT_URL",
    "http://dr-connect:8083"
)

def get_connectors():
    response = requests.get(f"{DR_CONNECT_URL}/connectors")
    response.raise_for_status()
    return response.json()

def validate_connector(name):

    response = requests.get(
        f"{DR_CONNECT_URL}/connectors/{name}/status"
    )

    response.raise_for_status()

    status = response.json()

    connector_state = status["connector"]["state"]

    if connector_state == "RUNNING":
        print(f"{name} is RUNNING")
        return True

    print(f"{name} is NOT RUNNING")
    return False

def validate_all():
    connectors = get_connectors()

    failed = []

    for connector in connectors:
        if not validate_connector(connector):
            failed.append(connector)

    if failed:
        raise Exception(
            f"Validation failed for: {failed}"
        )

if __name__ == "__main__":
    validate_all()
