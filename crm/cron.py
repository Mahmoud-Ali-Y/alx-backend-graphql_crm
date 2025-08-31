import logging
from datetime import datetime
import requests

def log_crm_heartbeat():
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    message = f"{timestamp} CRM is alive"

    # Append to log file
    with open(log_file, "a") as f:
        f.write(message + "\n")

    # Optional: check GraphQL hello endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"{message} - GraphQL responded: {response.json()}")
        else:
            print(f"{message} - GraphQL not responsive")
    except Exception as e:
        print(f"{message} - Error checking GraphQL: {e}")
    ["from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"]